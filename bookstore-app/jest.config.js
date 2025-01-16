module.exports = {
  preset: "ts-jest",
  testEnvironment: "jest-fixed-jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/tests/jest.setup.ts"],
  moduleNameMapper: {
    "\\.(css|scss)$": "<rootDir>/src/tests_mocks/styleMock.js",
    '\\.(png|jpe?g|gif|svg)$': '<rootDir>/src/tests_mocks/imageMock.js',
  },
};
