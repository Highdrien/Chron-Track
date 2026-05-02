import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import LoginPage from "./LoginPage";

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
      <LoginPage />
    </BrowserRouter>,
  );
}

describe("LoginPage", () => {
  it("renders the login form", () => {
    renderPage();
    expect(screen.getByText("Chron-Track")).toBeInTheDocument();
    expect(screen.getByLabelText("Nom d'utilisateur")).toBeInTheDocument();
    expect(screen.getByLabelText("Mot de passe")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Se connecter" }),
    ).toBeInTheDocument();
  });

  it("has a link to the register page", () => {
    renderPage();
    const link = screen.getByRole("link", { name: "Creer un compte" });
    expect(link).toHaveAttribute("href", "/register");
  });
});
