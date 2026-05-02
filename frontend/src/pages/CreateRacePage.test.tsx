import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import CreateRacePage from "./CreateRacePage";

function renderPage() {
  return render(
    <BrowserRouter>
      <CreateRacePage />
    </BrowserRouter>,
  );
}

describe("CreateRacePage", () => {
  it("renders the creation form with required fields", () => {
    renderPage();
    expect(screen.getByText("Nouvelle course")).toBeInTheDocument();
    expect(screen.getByLabelText("Nom *")).toBeInTheDocument();
    expect(screen.getByLabelText("Date *")).toBeInTheDocument();
    expect(screen.getByLabelText("Distance (km) *")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Creer la course" }),
    ).toBeInTheDocument();
  });

  it("renders optional fields section", () => {
    renderPage();
    expect(screen.getByLabelText("Lieu")).toBeInTheDocument();
    expect(screen.getByLabelText("Lien Strava")).toBeInTheDocument();
  });

  it("has cancel and back links to home", () => {
    renderPage();
    const links = screen.getAllByRole("link");
    const hrefs = links.map((l) => l.getAttribute("href"));
    expect(hrefs).toContain("/");
  });
});
