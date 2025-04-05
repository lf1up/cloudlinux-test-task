import type { Route } from "./+types/login";
import { Flex, Box, Button, TextField, Heading } from "@radix-ui/themes";

import Cookies from "js-cookie";

import API from "../api";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Appointments App" },
    { name: "description", content: "Login" },
  ];
}

export default function Login() {
  const login = () => {
    const loginURL = API.login;
    const email = document.querySelector('input[placeholder="Email"]')?.value;
    const password = document.querySelector('input[placeholder="Password"]')?.value;

    if (email && password) {
      fetch(loginURL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Login failed. Please check your credentials.");
        }
      })
      .then((data) => {
        Cookies.set("access_token", data.access);
        window.location.href = "/";
      })
      .catch((error) => {
        alert(error.message);
      });
    } else {
      alert("Please enter both email and password.");
    }
  };

  return (
    <Flex direction="column" gap="2" align="center" justify="center" style={{ height: "70vh" }}>
      <Heading>Login</Heading>
      <br />
      <Box maxWidth="250px">
        <TextField.Root size="2" placeholder="Email" />
      </Box>
      <Box maxWidth="250px">
        <TextField.Root size="2" placeholder="Password" />
      </Box>
      <br />
      <Button onClick={login}>Login</Button>
    </Flex>
  );
}