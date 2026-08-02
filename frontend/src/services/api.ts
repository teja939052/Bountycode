// Unified API surface. `src/services/api` resolves to this file first (before
// the `api/index.js` directory), so re-export the real aggregated object here
// to keep every import style (`../services/api`, `../services/api/index.js`)
// pointing at the same code.
import api from "./api/index.ts";
export * from "./api/index.ts";
export default api;
export { api };
