import { useState } from "react";

import type { UseHide } from "@/types/hooks";

export const useHide = (): UseHide => {
  const [hide, setHide] = useState<boolean>(false);

  const handleHide = (): void => {
    if (hide) {
      setHide(false);
      return;
    }

    setHide(true);
    return;
  };

  return {
    hide,
    handleHide,
  };
};
