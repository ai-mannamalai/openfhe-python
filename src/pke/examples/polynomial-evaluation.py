from openfhe import *
import time

def main():

    print("\n======EXAMPLE FOR EVALPOLY========\n")
    parameters = CCParamsCKKSRNS()
    parameters.SetMultiplicativeDepth(6)
    parameters.SetScalingModSize(50)

    cc = GenCryptoContext(parameters)
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)
    cc.Enable(PKESchemeFeature.ADVANCEDSHE)

    input = [complex(a,0) for a in [0.5, 0.7, 0.9, 0.95, 0.93]]
    # input = [0.5, 0.7, 0.9, 0.95, 0.93]
    encodedLength = len(input)
    coefficients1 = [0.15, 0.75, 0, 1.25, 0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 0, 1]
    coefficients2 = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5,
                    0.1, 0.2, 0.3, 0.4, 0.5, -0.1, -0.2, -0.3, -0.4, -0.5,
                    0.1, 0.2, 0.3, 0.4, 0.5, -0.1, -0.2, -0.3, -0.4, -0.5]
    plaintext1 = cc.MakeCKKSPackedPlaintext(input)

    keyPair = cc.KeyGen()
    
    print("Generating evaluation key for homomorphic multiplication...")
    cc.EvalMultKeyGen(keyPair.secretKey)
    print("Completed.\n")

    ciphertext1 = cc.Encrypt(keyPair.publicKey, plaintext1)

    t = time.time()
    result = cc.EvalPoly(ciphertext1, coefficients1)
    timeEvalPoly1 = time.time() - t

    t = time.time()
    result2 = cc.EvalPoly(ciphertext1, coefficients2)
    timeEvalPoly2 = time.time() - t

    plaintextDec = Decrypt(result, keyPair.secretKey)

    plaintextDec.SetLength(encodedLength)

    plaintextDec2 = Decrypt(result2, keyPair.secretKey)

    plaintextDec2.SetLength(encodedLength)

    print("\n Original Plaintext #1: \n")
    print(plaintext1)

    print(f"\n Result of evaluating a polynomial with coefficients {coefficients1}: \n")
    print(plaintextDec)

    print("\n Expected result: (0.70519107, 1.38285078, 3.97211180, "
                 "5.60215665, 4.86357575) \n") 

    print(f"\n Evaluation time: {timeEvalPoly1*1000} ms \n")

    print(f"\n Result of evaluating a polynomial with coefficients {coefficients2}: \n")
    print(plaintextDec2)  

    print("\n Expected result: (3.4515092326, 5.3752765397, 4.8993108833, "
                 "3.2495023573, 4.0485229982) \n")

    print(f"\n Evaluation time: {timeEvalPoly2*1000} ms \n")

if __name__ == '__main__':
    main() 
