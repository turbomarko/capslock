import DashboardContent from './DashboardContent';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white rounded-lg shadow">
            <div className="px-4 py-5 sm:p-6">
              <h1 className="text-2xl font-semibold text-gray-900 mb-6">
                Campaign Analysis Dashboard
              </h1>
              <DashboardContent />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
