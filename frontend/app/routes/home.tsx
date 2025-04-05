import type { Route } from "./+types/home";
import { Flex, Button, Heading, Box, TextField, Table } from "@radix-ui/themes";

import Cookies from "js-cookie";

import { login, logout, register, getAppointments, createAppointment, deleteAppointment } from "../utils";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Appointments App" },
    { name: "description", content: "Welcome to Appointments App!" },
  ];
}

export async function clientLoader({
  params,
}: Route.ClientLoaderArgs) {
  const accessToken = Cookies.get('access_token')

  if (!accessToken) {
    return [];
  }

  return await getAppointments(accessToken);
}

export default async function Home({
  loaderData,
}: Route.ComponentProps) {
  const accessToken = Cookies.get('access_token')

  const isUauthenticated = (
    <Flex direction="column" gap="2" align="center" justify="center" style={{ height: "70vh" }}>
      <Heading>Welcome to Appointments App! Please register or login.</Heading>
      <br />
      <Button onClick={login}>Login</Button>
      <Button onClick={register}>Register</Button>
    </Flex>
  );

  const isAuthenticated = (
    <Flex direction="column" gap="2" align="center" justify="center" style={{ height: "70vh" }}>
      <Heading>Welcome back! Here you might find some appointments.</Heading>
      <br />
      <Flex direction="row" gap="2">
        <Box maxWidth="250px">
          <TextField.Root size="2" placeholder="Notes..." />
        </Box>
        <Button onClick={() => createAppointment(
          accessToken,
          document.querySelector('input[placeholder="Notes..."]')?.value
        )}>Create Appointment</Button>
      </Flex>
      <br />
      {
        loaderData && loaderData.length > 0 ? (
          <Table.Root>
            <Table.Header>
              <Table.Row>
                <Table.ColumnHeaderCell>ID</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>Date</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>Email</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>Notes</Table.ColumnHeaderCell>
                <Table.ColumnHeaderCell>Action</Table.ColumnHeaderCell>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {loaderData.map((appointment) => (
                <Table.Row key={appointment.id}>
                  <Table.RowHeaderCell>{appointment.id}</Table.RowHeaderCell>
                  <Table.Cell>{new Date(appointment.date).toLocaleDateString()}</Table.Cell>
                  <Table.Cell>{appointment.user.email}</Table.Cell>
                  <Table.Cell>{appointment.notes}</Table.Cell>
                  <Table.Cell>
                    <Button onClick={() => deleteAppointment(accessToken, appointment.id)}>Delete</Button>
                  </Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>
        ) : (
          <p>No appointments found.</p>
        )
      }
      <br />
      <Button onClick={logout}>Logout</Button>
    </Flex>
  );

	return (
		accessToken ? isAuthenticated : isUauthenticated
	);
}
