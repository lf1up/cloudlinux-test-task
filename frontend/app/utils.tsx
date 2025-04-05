import Cookies from "js-cookie";

import API from "./api";

export const login = () => {
  window.location.href = "/login";
};

export const register = () => {
  window.location.href = "/register";
};

export const logout = () => {
  Cookies.remove('access_token');
  window.location.href = "/";
}

export const getAppointments = (accessToken) => {
  const appointmentsURL = API.getAppointments;

  return fetch(appointmentsURL, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${accessToken}`,
    },
  })
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("Failed to fetch appointments.");
    }
  })
  .then((data) => {
    return data;
  })
  .catch((error) => {
    console.error(error.message);
  });
}

export const createAppointment = (accessToken, text) => {
  const createAppointmentURL = API.createAppointment;

  fetch(createAppointmentURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ notes: text }),
  })
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("Failed to create appointment.");
    }
  })
  .then((data) => {
    window.location.href = "/";
  })
  .catch((error) => {
    console.error(error.message);
  });
}

export const deleteAppointment = (accessToken, id) => {
  const deteleAppointmentURL = API.deleteAppointment.replace(":id", id);

  fetch(deteleAppointmentURL, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${accessToken}`,
    },
  })
  .then((response) => {
    if (response.ok) {
      window.location.href = "/";
    } else {
      throw new Error("Failed to delete appointment.");
    }
  })
}