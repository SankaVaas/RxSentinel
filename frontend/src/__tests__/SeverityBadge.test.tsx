import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import SeverityBadge from "@/components/SeverityBadge";

describe("SeverityBadge", () => {
  it("renders the correct label for each severity", () => {
    render(<SeverityBadge severity="contraindicated" />);
    expect(screen.getByText("Contraindicated")).toBeInTheDocument();
  });
});
