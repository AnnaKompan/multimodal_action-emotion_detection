from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Early stop by val loss monitoring
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=20, # epochs without improvement
    restore_best_weights=True # back to best weights
)

# Reduce LR when a metric stopped improving
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5, # reduce lr by 50% 
    patience=10, # 10 epochs before reducing
    min_lr=1e-6 # 0,000001
)

# OR by training loss monitoring (not effective)

early_stop = EarlyStopping(
    monitor='loss',
    patience=20,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='loss',
    factor=0.5,
    patience=10,
    min_lr=1e-6
)

history = model.fit(
    X_train, y_train,
    epochs=500,
    callbacks=[tb_callback, early_stop, reduce_lr]  # TensorBoard callback
)

# OR split for val

history = model.fit(
    X_train, y_train,
    epochs=500,
    validation_split=0.1,   # 10% used as validation
    callbacks=[tb_callback, early_stop, reduce_lr]
)


sequences, labels = [], []

for action in actions:
    for sequence in range(no_sequences):
        window = []
        for frame_num in range(sequence_length):
            res = np.load(os.path.join(DATA_PATH, action, str(sequence), f"{frame_num}.npy"))
            window.append(res)

        # Always keep the original
        sequences.append(window)
        labels.append(label_map[action])

        # Now also add an augmented copy
        aug_window = []
        for frame in window:
            aug_window.append(augment_landmarks(frame))  # always apply augmentation
        aug_window = augment_sequence(aug_window)
        
        sequences.append(aug_window)
        labels.append(label_map[action])
