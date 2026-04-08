import "@testing-library/jest-dom";

import { TextDecoder, TextEncoder } from "util";

import { mockAssets } from "@tests/__mocks__/assets.mock";

const mockFetch = jest.fn();

Object.assign(globalThis, { TextEncoder, TextDecoder });

globalThis.fetch = mockFetch;

jest.mock("@/assets/export", () => ({
  __esModule: true,
  default: mockAssets,
}));
