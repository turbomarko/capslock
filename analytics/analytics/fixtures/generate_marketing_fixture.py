#!/usr/bin/env python3
"""
Marketing Campaign Data Generator for Django Fixtures
Generates realistic campaign performance data with built-in anomalies for testing.

Usage:
    python generate_marketing_fixture.py > fixtures/marketing_data.json
    python manage.py loaddata marketing_data.json
"""

import json
import random
import datetime
from decimal import Decimal
from typing import List, Dict, Any

# Configuration
START_DATE = datetime.date(2024, 1, 1)
END_DATE = datetime.date(2024, 6, 30)
TOTAL_DAYS = (END_DATE - START_DATE).days + 1

# Campaign configurations
CAMPAIGNS = [
    {
        "name": "Summer Fashion Collection",
        "platform": "Facebook",
        "objective": "conversions",
        "budget": 5000,
        "audience": "Women 25-40",
        "base_ctr": 2.5,
        "base_cpc": 1.20,
        "base_conversion_rate": 3.2,
    },
    {
        "name": "Tech Gadgets Q1",
        "platform": "Google",
        "objective": "traffic",
        "budget": 8000,
        "audience": "Tech Enthusiasts 20-35",
        "base_ctr": 3.1,
        "base_cpc": 2.50,
        "base_conversion_rate": 2.8,
    },
    {
        "name": "Local Restaurant Promo",
        "platform": "Instagram",
        "objective": "reach",
        "budget": 2000,
        "audience": "Local Food Lovers",
        "base_ctr": 1.8,
        "base_cpc": 0.80,
        "base_conversion_rate": 4.1,
    },
    {
        "name": "B2B Software Demo",
        "platform": "LinkedIn",
        "objective": "lead_generation",
        "budget": 12000,
        "audience": "Business Decision Makers",
        "base_ctr": 1.2,
        "base_cpc": 8.50,
        "base_conversion_rate": 5.5,
    },
    {
        "name": "Holiday Gift Guide",
        "platform": "Google",
        "objective": "sales",
        "budget": 15000,
        "audience": "Holiday Shoppers",
        "base_ctr": 2.8,
        "base_cpc": 1.80,
        "base_conversion_rate": 3.8,
    },
    {
        "name": "Fitness App Launch",
        "platform": "Facebook",
        "objective": "app_installs",
        "budget": 6000,
        "audience": "Fitness Enthusiasts",
        "base_ctr": 2.2,
        "base_cpc": 1.10,
        "base_conversion_rate": 12.0,  # Higher conversion rate for app installs
    },
    {
        "name": "Real Estate Showcase",
        "platform": "Instagram",
        "objective": "leads",
        "budget": 4000,
        "audience": "Home Buyers 30-50",
        "base_ctr": 1.5,
        "base_cpc": 3.20,
        "base_conversion_rate": 2.1,
    },
    {
        "name": "Educational Course Promo",
        "platform": "YouTube",
        "objective": "video_views",
        "budget": 3500,
        "audience": "Students & Professionals",
        "base_ctr": 4.2,
        "base_cpc": 0.65,
        "base_conversion_rate": 1.8,
    },
]

# Anomaly scenarios to inject
ANOMALIES = [
    {
        "campaign_name": "Summer Fashion Collection",
        "start_date": datetime.date(2024, 3, 15),
        "end_date": datetime.date(2024, 3, 20),
        "type": "ctr_drop",
        "description": "CTR drops due to ad fatigue",
        "impact": {"ctr_multiplier": 0.3, "cpc_multiplier": 1.4}
    },
    {
        "campaign_name": "Tech Gadgets Q1",
        "start_date": datetime.date(2024, 2, 10),
        "end_date": datetime.date(2024, 2, 12),
        "type": "cpc_spike",
        "description": "Competition increases CPC",
        "impact": {"cpc_multiplier": 2.5, "ctr_multiplier": 0.8}
    },
    {
        "campaign_name": "B2B Software Demo",
        "start_date": datetime.date(2024, 4, 1),
        "end_date": datetime.date(2024, 4, 7),
        "type": "conversion_drop",
        "description": "Landing page issues",
        "impact": {"conversion_rate_multiplier": 0.2, "cpc_multiplier": 1.1}
    },
    {
        "campaign_name": "Holiday Gift Guide",
        "start_date": datetime.date(2024, 5, 20),
        "end_date": datetime.date(2024, 5, 25),
        "type": "spend_spike",
        "description": "Budget auto-increase malfunction",
        "impact": {"spend_multiplier": 3.0, "impressions_multiplier": 2.5}
    },
    {
        "campaign_name": "Fitness App Launch",
        "start_date": datetime.date(2024, 1, 28),
        "end_date": datetime.date(2024, 2, 5),
        "type": "performance_boost",
        "description": "Viral social media mention",
        "impact": {"ctr_multiplier": 2.2, "conversion_rate_multiplier": 1.8, "impressions_multiplier": 1.5}
    }
]

class MarketingDataGenerator:
    def __init__(self):
        self.fixture_data = []
        self.campaign_id_counter = 1
        self.metric_id_counter = 1
        
    def add_model(self, model: str, pk: int, fields: Dict[str, Any]):
        """Add a model instance to the fixture data"""
        self.fixture_data.append({
            "model": model,
            "pk": pk,
            "fields": fields
        })
    
    def get_seasonal_multiplier(self, date: datetime.date, campaign_objective: str) -> float:
        """Apply seasonal trends based on date and campaign type"""
        month = date.month
        day_of_year = date.timetuple().tm_yday
        
        # Holiday shopping surge
        if campaign_objective in ["sales", "conversions"] and month in [11, 12]:
            return 1.4 + 0.3 * random.random()
        
        # Summer activity for lifestyle brands
        elif campaign_objective in ["reach", "app_installs"] and month in [6, 7, 8]:
            return 1.2 + 0.2 * random.random()
        
        # B2B campaigns slower in summer
        elif campaign_objective == "lead_generation" and month in [7, 8]:
            return 0.8 + 0.1 * random.random()
        
        # General weekly pattern (weekends typically lower performance)
        weekday = date.weekday()
        if weekday >= 5:  # Weekend
            return 0.85 + 0.2 * random.random()
        
        return 1.0 + 0.1 * (random.random() - 0.5)
    
    def get_anomaly_impact(self, campaign_name: str, date: datetime.date) -> Dict[str, float]:
        """Check if date falls within any anomaly period for the campaign"""
        for anomaly in ANOMALIES:
            if (anomaly["campaign_name"] == campaign_name and 
                anomaly["start_date"] <= date <= anomaly["end_date"]):
                return anomaly["impact"]
        return {}
    
    def generate_daily_metrics(self, campaign: Dict, campaign_id: int, date: datetime.date) -> Dict[str, Any]:
        """Generate realistic daily metrics for a campaign"""
        
        # Base metrics with some randomness
        seasonal_mult = self.get_seasonal_multiplier(date, campaign["objective"])
        anomaly_impact = self.get_anomaly_impact(campaign["name"], date)
        
        # Base impressions (varies by platform and budget)
        base_impressions = {
            "Facebook": 8000, "Instagram": 6000, "Google": 12000, 
            "LinkedIn": 3000, "YouTube": 15000
        }
        
        impressions = int(
            base_impressions.get(campaign["platform"], 8000) * 
            seasonal_mult * 
            anomaly_impact.get("impressions_multiplier", 1.0) *
            (0.8 + 0.4 * random.random())
        )
        
        # CTR calculation
        ctr = (
            campaign["base_ctr"] * 
            seasonal_mult * 
            anomaly_impact.get("ctr_multiplier", 1.0) *
            (0.7 + 0.6 * random.random())
        )
        ctr = max(0.1, min(ctr, 15.0))  # Keep within realistic bounds
        
        clicks = int(impressions * (ctr / 100))
        
        # CPC calculation
        cpc = (
            campaign["base_cpc"] * 
            anomaly_impact.get("cpc_multiplier", 1.0) *
            (0.8 + 0.4 * random.random())
        )
        cpc = max(0.10, cpc)
        
        spend = round(clicks * cpc, 2)
        
        # Daily budget constraint
        daily_budget = campaign["budget"] / 30  # Approximate daily budget
        spend = min(spend, daily_budget * anomaly_impact.get("spend_multiplier", 1.2))
        
        # Conversion rate and conversions
        conversion_rate = (
            campaign["base_conversion_rate"] * 
            seasonal_mult * 
            anomaly_impact.get("conversion_rate_multiplier", 1.0) *
            (0.6 + 0.8 * random.random())
        )
        conversion_rate = max(0.1, min(conversion_rate, 20.0))
        
        conversions = int(clicks * (conversion_rate / 100))
        
        # Calculate derived metrics
        cpa = round(spend / max(conversions, 1), 2)
        roas = round((conversions * 50) / max(spend, 1), 2) if spend > 0 else 0  # Assuming $50 avg order value
        
        return {
            "campaign": campaign_id,
            "date": date.isoformat(),
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "spend": str(spend),
            "ctr": round(ctr, 2),
            "cpc": round(cpc, 2),
            "cpa": cpa,
            "roas": roas,
            "device_breakdown": json.dumps({
                "mobile": round(random.uniform(0.4, 0.7), 2),
                "desktop": round(random.uniform(0.2, 0.4), 2),
                "tablet": round(random.uniform(0.05, 0.15), 2)
            }),
            "geography": json.dumps({
                "US": round(random.uniform(0.6, 0.8), 2),
                "CA": round(random.uniform(0.1, 0.2), 2),
                "UK": round(random.uniform(0.05, 0.15), 2),
                "Other": round(random.uniform(0.05, 0.15), 2)
            })
        }
    
    def generate_campaigns(self):
        """Generate campaign records"""
        for campaign in CAMPAIGNS:
            self.add_model("analytics.campaign", self.campaign_id_counter, {
                "name": campaign["name"],
                "platform": campaign["platform"],
                "objective": campaign["objective"],
                "start_date": START_DATE.isoformat(),
                "end_date": END_DATE.isoformat(),
                "budget": str(campaign["budget"]),
                "audience_segment": campaign["audience"],
                "status": "active" if random.random() > 0.1 else "paused",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            })
            self.campaign_id_counter += 1
    
    def generate_daily_metrics_for_all_campaigns(self):
        """Generate daily metrics for all campaigns"""
        current_date = START_DATE
        
        while current_date <= END_DATE:
            for i, campaign in enumerate(CAMPAIGNS, 1):
                
                # Some campaigns might not run every day
                if random.random() < 0.95:  # 95% chance of running each day
                    
                    metrics = self.generate_daily_metrics(campaign, i, current_date)
                    
                    self.add_model("analytics.dailymetric", self.metric_id_counter, metrics)
                    self.metric_id_counter += 1
            
            current_date += datetime.timedelta(days=1)
    
    def generate_analysis_results(self):
        """Generate some analysis results to show in dashboard"""
        analysis_results = [
            {
                "analysis_type": "anomaly_detection",
                "campaign": 1,  # Summer Fashion Collection
                "date_detected": "2024-03-15",
                "severity": "high",
                "metric_affected": "ctr",
                "description": "CTR dropped by 70% - possible ad fatigue",
                "recommendations": json.dumps([
                    "Refresh ad creative immediately",
                    "Test new audience segments",
                    "Consider reducing frequency cap"
                ]),
                "created_at": "2024-03-15T08:00:00Z"
            },
            {
                "analysis_type": "threshold_alert",
                "campaign": 2,  # Tech Gadgets Q1
                "date_detected": "2024-02-10",
                "severity": "medium",
                "metric_affected": "cpc",
                "description": "CPC increased by 150% - competition surge detected",
                "recommendations": json.dumps([
                    "Review bidding strategy",
                    "Expand keyword targeting",
                    "Consider dayparting optimizations"
                ]),
                "created_at": "2024-02-10T09:30:00Z"
            },
            {
                "analysis_type": "performance_alert",
                "campaign": 4,  # B2B Software Demo
                "date_detected": "2024-04-01",
                "severity": "critical",
                "metric_affected": "conversion_rate",
                "description": "Conversion rate dropped by 80% - landing page issues suspected",
                "recommendations": json.dumps([
                    "Check landing page functionality",
                    "Review form completion rates",
                    "Test page load speeds",
                    "Pause campaign until resolved"
                ]),
                "created_at": "2024-04-01T10:15:00Z"
            }
        ]
        
        for i, result in enumerate(analysis_results, 1):
            self.add_model("analytics.analysisresult", i, result)

    def generate_fixture(self) -> str:
        """Generate complete fixture data"""
        self.generate_campaigns()
        self.generate_daily_metrics_for_all_campaigns()
        self.generate_analysis_results()
        
        return json.dumps(self.fixture_data, indent=2)

def main():
    """Generate and output the fixture data"""
    generator = MarketingDataGenerator()
    fixture_json = generator.generate_fixture()
    
    print(fixture_json)
    
    # Print summary to stderr so it doesn't interfere with JSON output
    import sys
    print(f"\n# Generated fixture with:", file=sys.stderr)
    print(f"# - {len(CAMPAIGNS)} campaigns", file=sys.stderr)
    print(f"# - ~{TOTAL_DAYS * len(CAMPAIGNS)} daily metric records", file=sys.stderr)
    print(f"# - {len([a for a in ANOMALIES])} built-in anomalies", file=sys.stderr)
    print(f"# - Analysis results", file=sys.stderr)
    print(f"#", file=sys.stderr)
    print(f"# Usage:", file=sys.stderr)
    print(f"#   python generate_marketing_fixture.py > fixtures/marketing_data.json", file=sys.stderr)
    print(f"#   python manage.py loaddata marketing_data.json", file=sys.stderr)

if __name__ == "__main__":
    main()
