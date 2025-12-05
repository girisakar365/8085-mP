import { useConfirmDialog as useGlobalConfirmDialog, useSettingsActions } from '../../features/settings/stores/settingsStore';

export function useConfirmDialog() {
  const dialogState = useGlobalConfirmDialog();
  const { showConfirmDialog: showGlobalConfirm, closeConfirmDialog } = useSettingsActions();

  const showConfirm = ({
    title = 'Confirm Action',
    message,
    confirmText = 'Confirm',
    cancelText = 'Cancel',
    variant = 'danger',
  }) => {
    return new Promise((resolve) => {
      showGlobalConfirm({
        title,
        message,
        confirmText,
        cancelText,
        variant,
        onConfirm: () => {
          closeConfirmDialog();
          resolve(true);
        },
        onCancel: () => {
          closeConfirmDialog();
          resolve(false);
        },
      });
    });
  };

  const closeDialog = () => {
    closeConfirmDialog();
  };

  return {
    dialogState,
    showConfirm,
    closeDialog,
  };
}
