from qibo.models import Circuit
from qibo import gates
import numpy as np


class test_circuit:
    def __init__(self, nqubits, nlayers) -> None:
        self.nqubits = nqubits
        self.nlayers = nlayers

        
    def create_PQC(self):
        self.PQC = Circuit(self.nqubits)

    def create_QML(self):
        self.QML = Circuit(self.nqubits)



class single_qubit_and_entangling(test_circuit):
    def __init__(self, nqubits, nlayers):
        super().__init__(nqubits, nlayers)

        
    def create_PQC(self):
        super().create_PQC()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.PQC.add(gates.RX(q, theta = 0))
                self.PQC.add(gates.RZ(q, theta = 0))
                self.PQC.add(gates.RX(q, theta = 0))
            
            if l % 2 == 0:
                for q in range(0, self.nqubits, 2):
                    print(q)
                    self.PQC.add(gates.CNOT(q, (q+1) % (self.nqubits)))
            elif l % 2 != 0:
                for q in range(1, self.nqubits, 2):
                    self.PQC.add(gates.CNOT(q, (q+1) % (self.nqubits)))

        for q in range(self.nqubits):
                self.PQC.add(gates.RX(q, theta = 0))
                self.PQC.add(gates.RZ(q, theta = 0))
                self.PQC.add(gates.RX(q, theta = 0))


    def create_QML(self):
        super().create_QML()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
                self.QML.add(gates.RZ(q, theta = 0))
                self.QML.add(gates.RX(q, theta = 0))
            
            if l % 2 == 0:
                for q in range(0, self.nqubits, 2):
                    self.QML.add(gates.GPI((q + 1) % (self.nqubits), phi = 0).controlled_by(q))
            elif l % 2 != 0:
                for q in range(1, self.nqubits, 2):
                    self.QML.add(gates.GPI((q + 1) % self.nqubits, phi = 0).controlled_by(q))
                    
        for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
                self.QML.add(gates.RZ(q, theta = 0))
                self.QML.add(gates.RX(q, theta = 0))


    def mapper_QML(self, parameters, data):
        assert len(parameters) == len(self.PQC.get_parameters())
        
        self.PQC.set_parameters(parameters)

        data_parameters = np.zeros(len(self.QML.get_parameters()))


        index = 0
        for l in range(self.nlayers):
            data_parameters[index : index + 3 * self.nqubits] = \
                parameters[l * 3 * self.nqubits : (1 + l) * 3 * self.nqubits]
            
            index += 3 * self.nqubits
            
            if l % 2 == 0: size = len(list(range(0, self.nqubits, 2)))
            if l % 2 == 1: size = len(list(range(1, self.nqubits, 2)))
            
            data_parameters[index : index + size] = [data] * size
            index += size

        data_parameters[index : index + 3 * self.nqubits] = \
                parameters[self.nlayers * 3 * self.nqubits:]
        
        self.QML.set_parameters(data_parameters)
        return data_parameters



class single_qubit(test_circuit):
    def __init__(self, nqubits, nlayers):
        super().__init__(nqubits, nlayers)

        
    def create_PQC(self):
        super().create_PQC()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.PQC.add(gates.RX(q, theta = 0))
                self.PQC.add(gates.RZ(q, theta = 0))
                self.PQC.add(gates.RX(q, theta = 0))
            
        for q in range(self.nqubits):
                self.PQC.add(gates.RX(q, theta = 0))
                self.PQC.add(gates.RZ(q, theta = 0))
                self.PQC.add(gates.RX(q, theta = 0))


    def create_QML(self):
        super().create_QML()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
                self.QML.add(gates.RZ(q, theta = 0))
                self.QML.add(gates.RX(q, theta = 0))
            
            if l % 2 == 0:
                for q in range(0, self.nqubits, 2):
                    self.QML.add(gates.GPI((q + 1) % (self.nqubits), phi = 0).controlled_by(q))
            elif l % 2 != 0:
                for q in range(1, self.nqubits, 2):
                    self.QML.add(gates.GPI((q + 1) % self.nqubits, phi = 0).controlled_by(q))
                    
        for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
                self.QML.add(gates.RZ(q, theta = 0))
                self.QML.add(gates.RX(q, theta = 0))


    def mapper_QML(self, parameters, data):
        assert len(parameters) == len(self.PQC.get_parameters())
        
        self.PQC.set_parameters(parameters)

        data_parameters = np.zeros(len(self.QML.get_parameters()))


        index = 0
        for l in range(self.nlayers):
            data_parameters[index : index + 3 * self.nqubits] = \
                parameters[l * 3 * self.nqubits : (1 + l) * 3 * self.nqubits]
            
            index += 3 * self.nqubits
            
            if l % 2 == 0: size = len(list(range(0, self.nqubits, 2)))
            if l % 2 == 1: size = len(list(range(1, self.nqubits, 2)))
            
            data_parameters[index : index + size] = [data] * size
            index += size

        data_parameters[index : index + 3 * self.nqubits] = \
                parameters[self.nlayers * 3 * self.nqubits:]
        
        self.QML.set_parameters(data_parameters)
        return data_parameters



class permutation_simple(test_circuit):
    def __init__(self, nqubits, nlayers):
        super().__init__(nqubits, nlayers)

        
    def create_PQC(self):
        super().create_PQC()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.PQC.add(gates.RX(q, theta = 0))
            '''for q in range(0, self.nqubits, 2):
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.PQC.add(gates.RZ((q + 1) % (self.nqubits), phi = 0))
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
            for q in range(1, self.nqubits, 2):
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.PQC.add(gates.RZ((q + 1) % (self.nqubits), phi = 0))
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))'''
        
                    
            
            


    def create_QML(self):
        super().create_QML()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
            for q in range(0, self.nqubits, 2):
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.QML.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
            for q in range(1, self.nqubits, 2):
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.QML.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))


    def mapper_QML(self, parameters, data):
        assert len(parameters) == self.nlayers
        

        pqc_parameters = np.zeros(len(self.PQC.get_parameters()))
        qml_parameters = np.zeros(len(self.QML.get_parameters()))


        index = 0
        for l in range(self.nlayers):
            pqc_parameters[l * self.nqubits : (l + 1) * self.nqubits] = [parameters[l]] * self.nqubits 
            qml_parameters[index : index + self.nqubits] = [parameters[l]] * self.nqubits 
            index += self.nqubits
            qml_parameters[index : index + self.nqubits] = [data] * self.nqubits
            
            index += self.nqubits

        self.PQC.set_parameters(pqc_parameters)
        self.QML.set_parameters(qml_parameters)
        return pqc_parameters, qml_parameters


class permutation_double(test_circuit):
    def __init__(self, nqubits, nlayers):
        super().__init__(nqubits, nlayers)

        
    def create_PQC(self):
        super().create_PQC()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.PQC.add(gates.RX(q, theta = 0))
            for q in range(0, self.nqubits, 2):
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.PQC.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
            for q in range(1, self.nqubits, 2):
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.PQC.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
        

    def create_QML(self):
        super().create_QML()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
            for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
            for q in range(0, self.nqubits, 2):
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.QML.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
            for q in range(1, self.nqubits, 2):
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.QML.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))


    def mapper_QML(self, parameters, data):
        assert len(parameters) == 2 * self.nlayers
        

        pqc_parameters = np.zeros(len(self.PQC.get_parameters()))
        qml_parameters = np.zeros(len(self.QML.get_parameters()))


        index_pqc = 0
        index_qml = 0
        for i, p in enumerate(parameters):
            if i % 2 == 0:
                qml_parameters[index_qml : index_qml + self.nqubits] = [data] * self.nqubits 
                index_qml += self.nqubits

            pqc_parameters[index_pqc : index_pqc + self.nqubits] = [p] * self.nqubits 
            index_pqc += self.nqubits
            qml_parameters[index_qml : index_qml + self.nqubits] = [p] * self.nqubits 
            index_qml += self.nqubits
        
        self.PQC.set_parameters(pqc_parameters)
        self.QML.set_parameters(qml_parameters)
        return pqc_parameters, qml_parameters


class permutation_composed(test_circuit):
    def __init__(self, nqubits, nlayers):
        super().__init__(nqubits, nlayers)
    def create_PQC(self):
        super().create_PQC()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.PQC.add(gates.RX(q, theta = 0))
            for q in range(0, self.nqubits, 2):
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.PQC.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
            for q in range(1, self.nqubits, 2):
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.PQC.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.PQC.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
        

    def create_QML(self):
        super().create_QML()

        for l in range(self.nlayers):
            for q in range(self.nqubits):
                self.QML.add(gates.RY(q, theta = 0))
            for q in range(self.nqubits):
                self.QML.add(gates.RX(q, theta = 0))
            for q in range(0, self.nqubits, 2):
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.QML.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
            for q in range(1, self.nqubits, 2):
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))
                self.QML.add(gates.RZ((q + 1) % (self.nqubits), theta = 0))
                self.QML.add(gates.CNOT(q, (q + 1) % (self.nqubits)))


    def mapper_QML(self, parameters, data):
        assert len(parameters) == 2 * self.nlayers
        

        pqc_parameters = np.zeros(len(self.PQC.get_parameters()))
        qml_parameters = np.zeros(len(self.QML.get_parameters()))


        index_pqc = 0
        index_qml = 0
        for i, p in enumerate(parameters):
            if i % 2 == 0:
                qml_parameters[index_qml : index_qml + self.nqubits] = [data] * self.nqubits 
                index_qml += self.nqubits

            pqc_parameters[index_pqc : index_pqc + self.nqubits] = [p] * self.nqubits 
            index_pqc += self.nqubits
            qml_parameters[index_qml : index_qml + self.nqubits] = [p] * self.nqubits 
            index_qml += self.nqubits
        
        self.PQC.set_parameters(pqc_parameters)
        self.QML.set_parameters(qml_parameters)
        return pqc_parameters, qml_parameters