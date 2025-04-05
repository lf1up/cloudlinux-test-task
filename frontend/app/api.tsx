// API endpoints depends on environment (development, production etc.)
const API = {
  login: "http://127.0.0.1:8000/api/v1/login/",
  register: "http://127.0.0.1:8000/api/v1/register/",
  getAppointments: "http://127.0.0.1:8000/api/v1/appointments/",
  createAppointment: "http://127.0.0.1:8000/api/v1/appointments/create/",
  deleteAppointment: "http://127.0.0.1:8000/api/v1/appointments/:id/delete/",
  getAppointment: "http://127.0.0.1:8000/api/v1/appointments/:id/",
  createResponse: "http://127.0.0.1:8000/api/v1/responses/create/",
  updateResponse: "http://127.0.0.1:8000/api/v1/responses/:id/",
  deleteResponse: "http://127.0.0.1:8000/api/v1/responses/:id/delete/",
};

export default API;
