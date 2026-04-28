/**
 * Validation Context
 * Stores the validation result from the API so it can be shared
 * between the ValidateIdeaPage (which submits) and the ResultsPage (which displays).
 */

import { createContext, useContext, useState, type ReactNode } from "react";
import type { ValidationResponse } from "./api";

interface ValidationContextType {
  /** The most recent validation result, or null if none yet */
  result: ValidationResponse | null;
  /** Store a new validation result */
  setResult: (result: ValidationResponse | null) => void;
  /** Whether a validation is currently in progress */
  isLoading: boolean;
  /** Set the loading state */
  setIsLoading: (loading: boolean) => void;
  /** Any error message from the last validation attempt */
  error: string | null;
  /** Set an error message */
  setError: (error: string | null) => void;
}

const ValidationContext = createContext<ValidationContextType | undefined>(
  undefined
);

export function ValidationProvider({ children }: { children: ReactNode }) {
  const [result, setResult] = useState<ValidationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <ValidationContext.Provider
      value={{ result, setResult, isLoading, setIsLoading, error, setError }}
    >
      {children}
    </ValidationContext.Provider>
  );
}

export function useValidation() {
  const context = useContext(ValidationContext);
  if (context === undefined) {
    throw new Error("useValidation must be used within a ValidationProvider");
  }
  return context;
}
