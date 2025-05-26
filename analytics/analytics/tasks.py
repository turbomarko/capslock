from config import celery_app
from datetime import datetime, timedelta
from django.db import transaction
from analytics.models import Campaign, DailyMetric, AnalysisResult
import statistics
import logging
import httpx
import json
import aio_pika
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def analyze_campaign_performance(self, campaign_id=None, days_back=7):
    """
    Automated analysis task that detects anomalies and performance issues.
    
    Args:
        campaign_id: Specific campaign to analyze (None for all active campaigns)
        days_back: Number of days to look back for analysis
    
    Returns:
        dict: Analysis summary with alerts generated
    """
    try:
        # Get campaigns to analyze
        campaigns = Campaign.objects.filter(status='active')
        if campaign_id:
            campaigns = campaigns.filter(id=campaign_id)
        
        analysis_date = datetime.now().date()
        lookback_date = analysis_date - timedelta(days=days_back)
        
        alerts_generated = []
        
        for campaign in campaigns:
            logger.info(f"Analyzing campaign: {campaign.name}")
            
            # Get recent metrics
            recent_metrics = DailyMetric.objects.filter(
                campaign=campaign,
                date__gte=lookback_date,
                date__lte=analysis_date
            ).order_by('-date')
            
            if recent_metrics.count() < 3:
                continue  # Need at least 3 days of data
            
            # Perform anomaly detection
            ctr_anomaly = _detect_ctr_anomaly(recent_metrics, campaign)
            cpc_anomaly = _detect_cpc_anomaly(recent_metrics, campaign)
            spend_anomaly = _detect_spend_anomaly(recent_metrics, campaign)
            conversion_anomaly = _detect_conversion_anomaly(recent_metrics, campaign)
            
            # Check performance thresholds
            performance_alert = _check_performance_thresholds(recent_metrics, campaign)
            
            # Generate alerts for significant findings
            for anomaly in [ctr_anomaly, cpc_anomaly, spend_anomaly, conversion_anomaly, performance_alert]:
                if anomaly and anomaly['severity'] in ['medium', 'high', 'critical']:
                    alert = _create_analysis_result(campaign, anomaly, analysis_date)
                    if alert:
                        alerts_generated.append(alert)
        
        logger.info(f"Analysis complete. Generated {len(alerts_generated)} alerts.")
        
        return {
            'status': 'success',
            'campaigns_analyzed': campaigns.count(),
            'alerts_generated': len(alerts_generated),
            'alert_details': [
                {
                    'campaign': alert.campaign.name,
                    'severity': alert.severity,
                    'metric': alert.metric_affected,
                    'description': alert.description
                } for alert in alerts_generated
            ]
        }
        
    except Exception as exc:
        logger.error(f"Analysis task failed: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


def _detect_ctr_anomaly(metrics, campaign):
    """Detect CTR anomalies using statistical analysis"""
    ctr_values = [float(m.ctr) for m in metrics if m.ctr > 0]
    if len(ctr_values) < 3:
        return None
    
    recent_ctr = ctr_values[0]  # Most recent
    baseline_ctr = statistics.mean(ctr_values[1:])  # Previous days average
    
    # Check for significant drops (>40% decrease)
    if recent_ctr < baseline_ctr * 0.6:
        drop_percent = ((baseline_ctr - recent_ctr) / baseline_ctr) * 100
        return {
            'type': 'ctr_drop',
            'severity': 'high' if drop_percent > 60 else 'medium',
            'metric': 'ctr',
            'description': f"CTR dropped by {drop_percent:.1f}% - possible ad fatigue or audience saturation",
            'recommendations': [
                "Refresh ad creative immediately",
                "Test new audience segments", 
                "Review ad frequency and reduce if necessary"
            ]
        }
    
    return None


def _detect_cpc_anomaly(metrics, campaign):
    """Detect CPC spikes that indicate increased competition or bidding issues"""
    cpc_values = [float(m.cpc) for m in metrics if m.cpc > 0]
    if len(cpc_values) < 3:
        return None
    
    recent_cpc = cpc_values[0]
    baseline_cpc = statistics.mean(cpc_values[1:])
    
    # Check for significant increases (>50% increase)
    if recent_cpc > baseline_cpc * 1.5:
        increase_percent = ((recent_cpc - baseline_cpc) / baseline_cpc) * 100
        return {
            'type': 'cpc_spike',
            'severity': 'critical' if increase_percent > 100 else 'medium',
            'metric': 'cpc',
            'description': f"CPC increased by {increase_percent:.1f}% - competition surge or bidding issues",
            'recommendations': [
                "Review bidding strategy and adjust maximum bids",
                "Analyze competitor activity",
                "Consider expanding keyword targeting",
                "Implement dayparting to avoid peak competition hours"
            ]
        }
    
    return None


def _detect_spend_anomaly(metrics, campaign):
    """Detect unusual spending patterns"""
    spend_values = [float(m.spend) for m in metrics if m.spend > 0]
    if len(spend_values) < 3:
        return None
    
    recent_spend = spend_values[0]
    baseline_spend = statistics.mean(spend_values[1:])
    daily_budget = float(campaign.budget) / 30  # Approximate daily budget
    
    # Check for spend spikes (>200% of baseline or >150% of daily budget)
    if recent_spend > baseline_spend * 2 or recent_spend > daily_budget * 1.5:
        return {
            'type': 'spend_spike',
            'severity': 'high',
            'metric': 'spend',
            'description': f"Daily spend of ${recent_spend:.2f} is unusually high (baseline: ${baseline_spend:.2f})",
            'recommendations': [
                "Check for budget auto-increase settings",
                "Review bidding strategy for overspending",
                "Implement daily budget caps",
                "Monitor campaign throughout the day"
            ]
        }
    
    return None


def _detect_conversion_anomaly(metrics, campaign):
    """Detect conversion rate drops that might indicate landing page or tracking issues"""
    conversion_rates = []
    for m in metrics:
        if m.clicks > 0:
            conv_rate = (m.conversions / m.clicks) * 100
            conversion_rates.append(conv_rate)
    
    if len(conversion_rates) < 3:
        return None
    
    recent_conv_rate = conversion_rates[0]
    baseline_conv_rate = statistics.mean(conversion_rates[1:])
    
    # Check for significant drops (>50% decrease)
    if recent_conv_rate < baseline_conv_rate * 0.5 and baseline_conv_rate > 1:
        drop_percent = ((baseline_conv_rate - recent_conv_rate) / baseline_conv_rate) * 100
        return {
            'type': 'conversion_drop',
            'severity': 'critical',
            'metric': 'conversion_rate',
            'description': f"Conversion rate dropped by {drop_percent:.1f}% - landing page or tracking issues suspected",
            'recommendations': [
                "Check landing page functionality and load speed",
                "Verify conversion tracking setup",
                "Review form completion rates",
                "Test checkout/signup process",
                "Consider pausing campaign until resolved"
            ]
        }
    
    return None


def _check_performance_thresholds(metrics, campaign):
    """Check if key metrics are below acceptable thresholds"""
    if not metrics:
        return None
    
    latest_metric = metrics.first()
    
    # Platform-specific thresholds
    thresholds = {
        'Facebook': {'min_ctr': 1.0, 'max_cpa': 50, 'min_roas': 2.0},
        'Google': {'min_ctr': 2.0, 'max_cpa': 40, 'min_roas': 3.0}, 
        'Instagram': {'min_ctr': 1.2, 'max_cpa': 45, 'min_roas': 2.5},
        'LinkedIn': {'min_ctr': 0.8, 'max_cpa': 100, 'min_roas': 2.0},
        'YouTube': {'min_ctr': 3.0, 'max_cpa': 30, 'min_roas': 2.5}
    }
    
    platform_thresholds = thresholds.get(campaign.platform, thresholds['Facebook'])
    
    issues = []
    
    if latest_metric.ctr < platform_thresholds['min_ctr']:
        issues.append(f"CTR ({latest_metric.ctr}%) below threshold ({platform_thresholds['min_ctr']}%)")
    
    if latest_metric.cpa > platform_thresholds['max_cpa']:
        issues.append(f"CPA (${latest_metric.cpa}) above threshold (${platform_thresholds['max_cpa']})")
    
    if latest_metric.roas < platform_thresholds['min_roas']:
        issues.append(f"ROAS ({latest_metric.roas}) below threshold ({platform_thresholds['min_roas']})")
    
    if issues:
        return {
            'type': 'performance_threshold',
            'severity': 'medium',
            'metric': 'multiple',
            'description': f"Performance below thresholds: {'; '.join(issues)}",
            'recommendations': [
                "Review and optimize targeting parameters",
                "A/B test ad creative and copy",
                "Analyze top-performing audience segments",
                "Consider adjusting bidding strategy"
            ]
        }
    
    return None


@transaction.atomic
def _create_analysis_result(campaign, anomaly_data, analysis_date):
    """Create and save analysis result to database with LLM recommendations and notifications"""
    try:
        # Get LLM recommendations
        llm_recommendations = _get_llm_recommendations(campaign, anomaly_data)
        
        # Combine original recommendations with LLM recommendations
        all_recommendations = anomaly_data['recommendations'] + llm_recommendations
        
        analysis_result = AnalysisResult.objects.create(
            analysis_type=anomaly_data['type'],
            campaign=campaign,
            date_detected=analysis_date,
            severity=anomaly_data['severity'],
            metric_affected=anomaly_data['metric'],
            description=anomaly_data['description'],
            recommendations=all_recommendations
        )
        
        # Send notification
        _send_anomaly_notification(campaign, analysis_result)
        
        logger.info(f"Created analysis result: {analysis_result.id} for campaign {campaign.name}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Failed to create analysis result: {str(e)}")
        return None

def _get_llm_recommendations(campaign: Campaign, anomaly_data: Dict[str, Any]) -> List[str]:
    """Get additional recommendations from LLM service"""
    try:
        # Prepare the prompt for the LLM
        prompt = f"""
        Campaign: {campaign.name}
        Platform: {campaign.platform}
        Issue Type: {anomaly_data['type']}
        Severity: {anomaly_data['severity']}
        Metric Affected: {anomaly_data['metric']}
        Description: {anomaly_data['description']}
        
        Based on this campaign anomaly, provide 2-3 specific, actionable recommendations 
        for improving campaign performance. Focus on practical steps that can be taken 
        immediately. Format each recommendation as a separate item.
        """
        
        # Call LLM service
        response = httpx.post(
            "http://llm:8000/chat",
            json={
                "messages": [
                    {"role": "system", "content": "You are a digital marketing expert providing campaign optimization advice."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        
        # Parse and format recommendations
        llm_response = response.json()
        recommendations = [
            rec.strip() for rec in llm_response['response'].split('\n')
            if rec.strip() and not rec.strip().startswith(('Based on', 'Here are', 'Recommendations:'))
        ]
        
        return recommendations[:3]  # Limit to top 3 recommendations
        
    except Exception as e:
        logger.error(f"Failed to get LLM recommendations: {str(e)}")
        return []

def _send_anomaly_notification(campaign: Campaign, analysis_result: AnalysisResult):
    """Send notification about the anomaly via RabbitMQ"""
    try:
        # Connect to RabbitMQ
        connection = aio_pika.connect_robust(
            "amqp://guest:guest@rabbitmq:5672/"
        )
        
        # Prepare notification message
        notification = {
            "to_email": campaign.owner_email,  # Assuming this field exists in Campaign model
            "subject": f"Campaign Alert: {analysis_result.severity.upper()} - {campaign.name}",
            "body": f"""
            Campaign Alert: {analysis_result.severity.upper()}
            
            Campaign: {campaign.name}
            Platform: {campaign.platform}
            Issue Type: {analysis_result.analysis_type}
            Metric Affected: {analysis_result.metric_affected}
            
            Description:
            {analysis_result.description}
            
            Recommendations:
            {chr(10).join(f'- {rec}' for rec in analysis_result.recommendations)}
            
            Please review and take appropriate action.
            """
        }
        
        # Send message to RabbitMQ
        channel = connection.channel()
        queue = channel.declare_queue("notifications")
        channel.basic_publish(
            aio_pika.Message(body=json.dumps(notification).encode()),
            routing_key="notifications"
        )
        
        logger.info(f"Sent notification for analysis result: {analysis_result.id}")
        
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
