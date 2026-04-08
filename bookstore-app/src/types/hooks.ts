export interface UseForm<T> {
  formState: T;
  onInputChange: React.ChangeEventHandler<HTMLInputElement | HTMLTextAreaElement>;
  onResetForm: () => void;
}

export interface UseHide {
  hide: boolean;
  handleHide: () => void;
}
