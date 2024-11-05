import { useEffect, useState } from "react";

type UseForm<T> = {
  formState: T;
  onInputChange: React.ChangeEventHandler<
    HTMLInputElement | HTMLTextAreaElement
  >;
  onResetForm: () => void;
};

export const useForm = <T,>(initialForm: T): UseForm<T> => {
  const [formState, setFormState] = useState<T>(initialForm);

  const onInputChange: React.ChangeEventHandler<
    HTMLInputElement | HTMLTextAreaElement
  > = ({ target }) => {
    const { name, value } = target;

    setFormState({
      ...formState,
      [name]: value,
    });
  };

  const onResetForm = (): void => {
    setFormState(initialForm);
  };

  useEffect(() => {
    if (!formState) {
      setFormState(initialForm);
    }
  }, [initialForm]);

  return {
    formState,
    onInputChange,
    onResetForm,
  };
};
