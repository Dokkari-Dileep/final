import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models  
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau  
import numpy as np
import matplotlib.pyplot as plt
import os
import json

# Configuration
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
NUM_CLASSES = 50  # Adjust based on your dataset
DATA_DIR = 'dataset'  # Update this path

# Create data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)

print("📊 Creating data generators...")
train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

validation_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Get class names
class_names = list(train_generator.class_indices.keys())
print(f"✅ Found {len(class_names)} classes")
print(f"Classes: {class_names}")

# Save class names for later use
with open('class_names.json', 'w') as f:     
    json.dump(class_names, f)

# Create the model
def create_model(num_classes):
    # Load EfficientNetB0 with pre-trained ImageNet weights
    base_model = EfficientNetB0(
        include_top=False,
        weights='imagenet',
        input_shape=(224, 224, 3),
        pooling='avg'
    )

    # Freeze base model layers
    base_model.trainable = False

    # Create new model on top
    inputs = keras.Input(shape=(224, 224, 3))
    x = base_model(inputs, training=False)   
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(512, activation='relu')(x)
    x = layers.BatchNormalization()(x)       
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    model = keras.Model(inputs, outputs)     

    # Compile the model - FIXED: removed AUC metric
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',     
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )

    return model

# Create model
model = create_model(len(class_names))       
model.summary()

# Callbacks
callbacks = [
    EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
    ModelCheckpoint('model/best_model.h5', monitor='val_accuracy', save_best_only=True),  
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-6)
]

print("🚀 Training model...")
# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    validation_data=validation_generator,    
    validation_steps=validation_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1
)

# Save the final model
model.save('model/disease_model.h5')

# Plot training history
def plot_training_history(history):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Accuracy
    axes[0, 0].plot(history.history['accuracy'], label='Training Accuracy')
    axes[0, 0].plot(history.history['val_accuracy'], label='Validation Accuracy')
    axes[0, 0].set_title('Model Accuracy')   
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')        
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    # Loss
    axes[0, 1].plot(history.history['loss'], label='Training Loss')
    axes[0, 1].plot(history.history['val_loss'], label='Validation Loss')
    axes[0, 1].set_title('Model Loss')       
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    # Precision
    axes[1, 0].plot(history.history['precision'], label='Training Precision')
    axes[1, 0].plot(history.history['val_precision'], label='Validation Precision')       
    axes[1, 0].set_title('Model Precision')  
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Precision')       
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    # Recall
    axes[1, 1].plot(history.history['recall'], label='Training Recall')
    axes[1, 1].plot(history.history['val_recall'], label='Validation Recall')
    axes[1, 1].set_title('Model Recall')     
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Recall')
    axes[1, 1].legend()
    axes[1, 1].grid(True)

    plt.tight_layout()
    plt.savefig('model/training_history.png')
    plt.show()

plot_training_history(history)

# Evaluate the model
print("\nEvaluating model on validation set...")
val_loss, val_accuracy, val_precision, val_recall = model.evaluate(validation_generator)  
print(f"Validation Accuracy: {val_accuracy:.2%}")
print(f"Validation Precision: {val_precision:.2%}")
print(f"Validation Recall: {val_recall:.2%}")

# Calculate F1 Score
val_f1 = 2 * (val_precision * val_recall) / (val_precision + val_recall)
print(f"Validation F1 Score: {val_f1:.2%}")  

# Save evaluation metrics
metrics = {
    'accuracy': float(val_accuracy),
    'precision': float(val_precision),       
    'recall': float(val_recall),
    'f1_score': float(val_f1)
}

with open('model/evaluation_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("\n🎉 Model training completed!")
print("Model saved as 'model/disease_model.h5'")
