import { useState } from "react";

export type UseHide = {
  hide: boolean;
  handleHide: () => void;
};

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
