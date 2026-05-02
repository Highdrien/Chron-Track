import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import RegisterPage from "./RegisterPage";

vi.mock("../context/AuthContext", () => ({
  useAuth: () => ({
    login: vi.fn(),
    user: null,
    loading: false,
    register: vi.fn(),
    logout: vi.fn(),
  }),
}));

function renderPage() {
  return render(
    <BrowserRouter>
      <RegisterPage />
    </BrowserRouter>,
  );
}

describe("RegisterPage", () => {
  it("renders the registration form", () => {
    renderPage();
    expect(screen.getByLabelText("Nom d'utilisateur")).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Mot de passe")).toBeInTheDocument();
    expect(
      screen.getByLabelText("Confirmer le mot de passe"),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Creer un compte" }),
    ).toBeInTheDocument();
  });

  it("has a link to the login page", () => {
    renderPage();
    const link = screen.getByRole("link", { name: "Se connecter" });
    expect(link).toHaveAttribute("href", "/login");
  });
});
