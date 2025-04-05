import type { Route } from "./+types/register";

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Appointments App" },
    { name: "description", content: "Registration" },
  ];
}

export default function Register() {
  return (
    <div>
      <h1>[UNIMPLEMENTED] Please register!</h1>
      <p>Or use 'admin / admin' for testing purposes :)</p>
    </div>
  );
}