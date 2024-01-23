**Folgendes neuronales Netz wurde verwendet:**

Model: "sequential"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
 
=================================================================
 dense (Dense)               (None, 20)                500       
                                                                 
 dense_1 (Dense)             (None, 20)                420       
                                                                 
 dense_2 (Dense)             (None, 1)                 21        
                                                                 
=================================================================
Total params: 941 (3.68 KB)
Trainable params: 941 (3.68 KB)
Non-trainable params: 0 (0.00 Byte)
_________________________________________________________________


Epochen: 30

MAE:  2.4973567708077318

Mögliche Verbesserungen: 
- Nutzen eines RNN um die Zeitreihendaten besser zu berücksichtigen.
