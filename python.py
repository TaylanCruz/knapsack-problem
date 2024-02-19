import sys

def knapSack(W, V, pacotes, n, placa, golden_output): 
    K = [[[0 for x in range(V + 1)] for x in range(W + 1)] for x in range(n + 1)] 
  
    for i in range(n + 1): 
        for w in range(W + 1): 
            for v in range(V + 1):
                if i == 0 or w == 0 or v == 0: 
                    K[i][w][v] = 0
                elif pacotes[i-1]['peso'] <= w and pacotes[i-1]['volume'] <= v and pacotes[i-1]['status'] == 'PENDENTE': 
                    K[i][w][v] = max(pacotes[i-1]['valor'] 
                                + K[i-1][w-pacotes[i-1]['peso']][v-pacotes[i-1]['volume']], 
                                K[i-1][w][v]) 
                else: 
                    K[i][w][v] = K[i-1][w][v] 
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

    golden_input = open(sys.argv[1],'r')
    golden_output = open(sys.argv[2],'w')

    n_carros = int(golden_input.readline())
    carros = []
    for i in range(n_carros):
        placa, peso, volume = golden_input.readline().split()
        carros.append({"placa": placa, "peso": int(peso), "volume": int(volume)})
    
    n_pacotes = int(golden_input.readline())
    pacotes = []
    for _ in range(n_pacotes):
        codigo, valor, peso, volume = golden_input.readline().split()
        pacotes.append({"codigo": codigo, 
                        "valor": float(valor), 
                        "peso": int(peso), 
                        "volume": int(volume),
                        "status": "PENDENTE"})
    for c in carros:
        knapSack(c['peso'], c['volume'], pacotes, n_pacotes, c['placa'], golden_output)
    for p in pacotes:
        if p['status'] == 'PENDENTE':
            golden_output.write(f'[PENDENTE] R$ {p["valor"]:.2f}, {p["peso"]} KG, {p["volume"]}L\n')
            golden_output.write(p['codigo'] + '\n')


    golden_input.close()
    golden_output.close()

if __name__ == '__main__':
    main(sys.argv)