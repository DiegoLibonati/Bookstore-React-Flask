export type UseForm<T> = {
  formState: T;
  onInputChange: React.ChangeEventHandler<
    HTMLInputElement | HTMLTextAreaElement
  >;
  onResetForm: () => void;
};

export type UseHide = {
  hide: boolean;
  handleHide: () => void;
};
