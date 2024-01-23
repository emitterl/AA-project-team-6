**Folgendes neuronales Netz wurde verwendet:**


1 Input Layer
4 Hidden Layer
1 Output Layer

--> Dropout Layer ro prevent overfitting


Model: "sequential"
_________________________________________________________________

 Layer (type)                Output Shape              Param #   
 
=================================================================

 dense (Dense)               (None, 25)                625       
                                                                 
 dropout (Dropout)           (None, 25)                0         
                                                                 
 dense_1 (Dense)             (None, 25)                650       
                                                                 
 dropout_1 (Dropout)         (None, 25)                0         
                                                                 
 dense_2 (Dense)             (None, 25)                650       
                                                                 
 dense_3 (Dense)             (None, 1)                 26            
                                                                 
=================================================================
Total params: 1951 (7.62 KB)
Trainable params: 1951 (7.62 KB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________

Epochen: 30

MSE:  16.05473765646475
MAE:  2.041645296336691

Mögliche Verbesserungen: 
- Nutzen eines RNN um die Zeitreihendaten besser zu berücksichtigen.
