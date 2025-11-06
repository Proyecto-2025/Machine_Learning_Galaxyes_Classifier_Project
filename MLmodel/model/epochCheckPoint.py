from tensorflow.keras.callbacks import Callback
import matplotlib.pyplot as plt
import os

class EpochCheckpoint(Callback):
    def __init__(self, save_interval=50, file_name="galaxy_model", checkpoints_dir="checkpoints", plots_dir="plots"):
        super().__init__()
        self.save_interval = save_interval
        self.checkpoints_dir = checkpoints_dir
        self.plots_dir = plots_dir
        self.file_name = file_name

        os.makedirs(self.checkpoints_dir, exist_ok=True)
        os.makedirs(self.plots_dir, exist_ok=True)

    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % self.save_interval == 0:
            # save model
            modfilename = self.checkpoints_dir + f"/{self.file_name}_epoch_{epoch + 1:03d}.h5"
            figfilename = self.plots_dir + f"/{self.file_name}_epoch_{epoch + 1:03d}.png"
            self.model.save(modfilename)
            print(f"\n✅ Saved model at epoch {epoch + 1} -> {modfilename}")

            # save loss and accuracy curves
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

            # Loss plot
            ax1.plot(self.model.history.history['loss'], label='train_loss')
            ax1.plot(self.model.history.history['val_loss'], label='val_loss')

            # Mark minimum val_loss point
            val_losses = self.model.history.history['val_loss']
            min_val_loss_epoch = val_losses.index(min(val_losses))
            min_val_loss = min(val_losses)
            ax1.plot(min_val_loss_epoch, min_val_loss, 'r*', markersize=15,
                     label=f'Min val_loss: {min_val_loss:.4f} (epoch {min_val_loss_epoch + 1})')

            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Loss')
            ax1.set_title('Loss Curves')
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # Accuracy plot
            ax2.plot(self.model.history.history['accuracy'], label='train_accuracy')
            ax2.plot(self.model.history.history['val_accuracy'], label='val_accuracy')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Accuracy')
            ax2.set_title('Accuracy Curves')
            ax2.legend()
            ax2.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(figfilename)
            plt.close()
            print(f"📉 Saved loss and accuracy curves at epoch {epoch + 1}")
            print(f"⭐ Best val_loss: {min_val_loss:.4f} at epoch {min_val_loss_epoch + 1}")