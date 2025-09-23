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
