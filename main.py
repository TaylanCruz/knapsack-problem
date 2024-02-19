import sys

# K = []

def calc(W, V, pacotes, n, K):
    # base conditions 
    if n == 0 or W == 0 or V == 0: 
        return 0
    if K[n][W][V] != -1: 
        return K[n][W][V]
  
    # choice diagram code 
    if pacotes[n-1]['peso'] <= W and pacotes[n-1]['volume'] <= V and pacotes[n-1]['status'] == 'PENDENTE': 
        K[n][W][V] = max( 
            pacotes[n-1]['valor']  + calc( 
                W-pacotes[n-1]['peso'], V-pacotes[n-1]['volume'], pacotes, n-1, K), 
            calc(W, V, pacotes, n-1, K)) 
        return K[n][W][V] 
    else: 
        K[n][W][V] = calc(W, V, pacotes, n-1, K) 
        return K[n][W][V] 

def knapSack(W, V, pacotes, n, placa, golden_output, K): 
    # K = [[[0 for x in range(V + 1)] for x in range(W + 1)] for x in range(n + 1)] 
    # global K
    # print(K)
    # for i in range(n + 1): 
    #     for w in range(W + 1): 
    #         for v in range(V + 1):
    #             if i == 0 or w == 0 or v == 0: 
    #                 K[i][w][v] = 0
    #             elif pacotes[i-1]['peso'] <= w and pacotes[i-1]['volume'] <= v and pacotes[i-1]['status'] == 'PENDENTE': 
    #                 K[i][w][v] = max(pacotes[i-1]['valor'] 
    #                             + K[i-1][w-pacotes[i-1]['peso']][v-pacotes[i-1]['volume']], 
    #                             K[i-1][w][v]) 
    #             else: 
    #                 K[i][w][v] = K[i-1][w][v] 
    calc(W, V, pacotes, n, K)
    res = K[n][W][V]
    w = W
    v = V
    i = n
    codigos = []
    while i > 0 and res > 0:
        if res == K[i-1][w][v]:
            pass
        else:
            codigos.append(pacotes[i-1]['codigo'])
            res -= pacotes[i-1]['valor']
            w -= pacotes[i-1]['peso']
            v -= pacotes[i-1]['volume']
            pacotes[i-1]['status'] = 'ARMAZENADO'
        i -= 1 
    golden_output.write(f"[{placa}] R$ {K[n][W][V]:.2f}, {W-w} KG ({(W-w)/W*100:.2f}%), {V-v}L ({(V-v)/V*100:.2f}%)\n")
    for c in codigos:
        golden_output.write(c + '\n')
    return K[n][W][V] 

def main(args):
    #Ilustrando uso de argumentos de programa
    # print("#ARGS = %i"%len((args)))
    # print("PROGRAMA = %s"%(args[0]))
    # print("ARG1 = %s, ARG2 = %s" %(args[1], args[2]))
    #Abrindo Arquivos
    golden_input = open(sys.argv[1],'r')
    golden_output = open(sys.argv[2],'w')

    n_carros = int(golden_input.readline())
    carros = []
    peso_maximo = 0
    volume_maximo = 0
    for i in range(n_carros):
        placa, peso, volume = golden_input.readline().split()
        carros.append({"placa": placa, "peso": int(peso), "volume": int(volume)})
        peso_maximo = max(peso_maximo, int(peso))
        volume_maximo = max(volume_maximo, int(volume))
    
    n_pacotes = int(golden_input.readline())
    pacotes = []
    for _ in range(n_pacotes):
        codigo, valor, peso, volume = golden_input.readline().split()
        pacotes.append({"codigo": codigo, 
                        "valor": float(valor), 
                        "peso": int(peso), 
                        "volume": int(volume),
                        "status": "PENDENTE"})
     
    # print(K)
    # print(pacotes)
    for c in carros:
        K = [[[-1 for x in range(volume_maximo + 1)] for x in range(peso_maximo + 1)] for x in range(n_pacotes + 1)]
        knapSack(c['peso'], c['volume'], pacotes, n_pacotes, c['placa'], golden_output, K)
        # print(pacotes)
    for p in pacotes:
        if p['status'] == 'PENDENTE':
            golden_output.write(f'[PENDENTE] R$ {p["valor"]:.2f}, {p["peso"]} KG, {p["volume"]}L\n')
            golden_output.write(p['codigo'] + '\n')

    #
    # ...
    #
    #fechando arquivos
    golden_input.close()
    golden_output.close()

#Finalizando programa
if __name__ == '__main__':
    main(sys.argv)