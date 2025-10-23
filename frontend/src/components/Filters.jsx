import { useState } from 'react';

function Filters({ locations, metrics, filters, onFilterChange, onApplyFilters }) {
  // TODO: Implement the filters component that allows users to:
  // - [x] Select a location from the available locations
  // - [x] Select a climate metric from available metrics
  // - Choose a date range (start and end dates)
  // - Filter by data quality threshold
  // - Select different analysis types
  // - [x] Apply the filters
  //
  // Requirements:
  // - Use the locations and metrics arrays passed as props
  // - Maintain filter state
  // - Call onFilterChange when filters change
  // - Call onApplyFilters when filters should be applied
  // - Use appropriate UI components (dropdowns, date pickers, etc.)
  // - Make the UI responsive and user-friendly
  // - Add any additional filtering options you think would be valuable

  const handleFilterChange = (updatedFilter) => {
    onFilterChange({ ...filters, ...updatedFilter });
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-eco-primary mb-4">Filter Data</h2>
      <select value={filters.locationId} onChange={(e) => handleFilterChange({ locationId: e.target.value })}>
        <option key="all" value="">All Locations</option>
        {locations.map(loc => (
          <option key={loc.id} value={loc.id}>{loc.name}</option>
        ))}
      </select>
      <select value={filters.metric} onChange={(e) => handleFilterChange({ metric: e.target.value })}>
        <option key="all" value="">All Metrics</option>
        {metrics.map(metric => (
          <option key={metric.id} value={metric.name}>{metric.display_name}</option>
        ))}
      </select>
      <select value={filters.analysisType} onChange={(e) => handleFilterChange({ analysisType: e.target.value })}>
        <option value="raw">Raw</option>
        <option value="weighted">Weighted</option>
        <option value="trends">Trends</option>
      </select>
      <button onClick={onApplyFilters}>Apply</button>
    </div >
  );
}

export default Filters;