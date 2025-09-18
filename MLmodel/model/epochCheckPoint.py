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
            modfilename = self.checkpoints_dir + f"/{self.file_name}_epoch_{epoch+1:03d}.h5"
            figfilename = self.plots_dir + f"/{self.file_name}_epoch_{epoch+1:03d}.png"
            self.model.save(modfilename)
            print(f"\n✅ Saved model at epoch {epoch+1} -> {modfilename}")
            
            # save loss curve snapshot
            plt.plot(self.model.history.history['loss'], label='train_loss')
            plt.plot(self.model.history.history['val_loss'], label='val_loss')
            plt.legend()
            plt.savefig(figfilename)
            plt.close()
            print(f"📉 Saved loss curve at epoch {epoch+1}")
