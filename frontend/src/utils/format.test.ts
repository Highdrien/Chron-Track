import { describe, expect, it } from "vitest";
import { formatDuration, formatPace, parseDurationToSeconds } from "./format";

describe("parseDurationToSeconds", () => {
  it("parses HH:MM:SS format", () => {
    expect(parseDurationToSeconds("01:25:22")).toBe(5122);
    expect(parseDurationToSeconds("00:32:05")).toBe(1925);
  });

  it("parses ISO 8601 duration format", () => {
    expect(parseDurationToSeconds("P0DT01H25M22S")).toBe(5122);
    expect(parseDurationToSeconds("P0DT0H32M5S")).toBe(1925);
  });

  it("handles days in ISO 8601", () => {
    expect(parseDurationToSeconds("P1DT02H00M00S")).toBe(86400 + 7200);
  });

  it("handles missing parts in ISO 8601", () => {
    expect(parseDurationToSeconds("PT30M")).toBe(1800);
    expect(parseDurationToSeconds("PT1H")).toBe(3600);
    expect(parseDurationToSeconds("PT45S")).toBe(45);
  });

  it("returns 0 for empty or unparseable strings", () => {
    expect(parseDurationToSeconds("")).toBe(0);
    expect(parseDurationToSeconds("garbage")).toBe(0);
  });
});

describe("formatDuration", () => {
  it("formats HH:MM:SS into human-readable", () => {
    expect(formatDuration("01:25:22")).toBe("1h25m22s");
    expect(formatDuration("00:32:05")).toBe("32m05s");
  });

  it("formats ISO 8601 duration into human-readable", () => {
    expect(formatDuration("P0DT01H25M22S")).toBe("1h25m22s");
    expect(formatDuration("P0DT0H32M5S")).toBe("32m05s");
  });

  it("returns raw string when unparseable", () => {
    expect(formatDuration("unknown")).toBe("unknown");
  });

  it("pads minutes and seconds", () => {
    expect(formatDuration("P0DT2H3M4S")).toBe("2h03m04s");
  });
});

describe("formatPace", () => {
  it("formats decimal pace into min'sec format", () => {
    expect(formatPace("5.5")).toBe("5'30\"");
    expect(formatPace("4.25")).toBe("4'15\"");
    expect(formatPace("6.0")).toBe("6'00\"");
  });

  it("returns raw string for non-numeric input", () => {
    expect(formatPace("abc")).toBe("abc");
  });
});
