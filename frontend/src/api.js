/**
 * API service module for making requests to the backend
 */

const API_BASE_URL = `${import.meta.API_URL}/api/v1`;

/**
 * Fetch climate data with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getClimateData = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams({
        ...(filters.locationId && { location_id: filters.locationId }),
        ...(filters.startDate && { start_date: filters.startDate }),
        ...(filters.endDate && { end_date: filters.endDate }),
        ...(filters.metric && { metric: filters.metric }),
        ...(filters.qualityThreshold && { quality_threshold: filters.qualityThreshold })
      });
    const url = API_BASE_URL + '/climate?' + queryParams
    const res = await fetch(url);
    if (!res.ok) {
      throw Error(res.status)
    }
    return res
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Fetch all available locations
 * @returns {Promise} - API response
 */
export const getLocations = async () => {
  try {
    const url = `${API_BASE_URL}/locations`
    const res = await fetch(url);
    if (!res.ok) {
      throw Error(res.status)
    }
    return res
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Fetch all available metrics
 * @returns {Promise} - API response
 */
export const getMetrics = async () => {
  try {
    const url = `${API_BASE_URL}/metrics`
    const res = await fetch(url);
    if (!res.ok) {
      throw Error(res.status)
    }
    return res
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Fetch climate summary statistics with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getClimateSummary = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams({
        ...(filters.locationId && { location_id: filters.locationId }),
        ...(filters.startDate && { start_date: filters.startDate }),
        ...(filters.endDate && { end_date: filters.endDate }),
        ...(filters.metric && { metric: filters.metric }),
        ...(filters.qualityThreshold && { quality_threshold: filters.qualityThreshold })
      });
    const url = API_BASE_URL + '/summary?' + queryParams 
    const res = await fetch(url);
    if (!res.ok) {
      throw Error(res.status)
    }
    return res
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

/**
 * Fetch climate trends with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getClimateTrends = async (filters = {}) => {
  try {
    const queryParams = new URLSearchParams({
        ...(filters.locationId && { location_id: filters.locationId }),
        ...(filters.startDate && { start_date: filters.startDate }),
        ...(filters.endDate && { end_date: filters.endDate }),
        ...(filters.metric && { metric: filters.metric }),
        ...(filters.qualityThreshold && { quality_threshold: filters.qualityThreshold })
      });
    const url = API_BASE_URL + '/trends?' + queryParams
    const res = await fetch(url);
    if (!res.ok) {
      throw Error(res.status)
    }
    return res
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}