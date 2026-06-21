from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Paciente:
    cedula: str
    nombres: str
    edad: int
    telefono: str

@dataclass
class Turno:
    codigo: int
    cedula_paciente: str
    fecha: str
    hora: str
    especialidad: str
    medico: str
    estado: str = "Agendado"

class AgendaClinica:
    def __init__(self):
        self.pacientes: List[Paciente] = []  # vector de registros
        self.turnos: List[Turno] = []        # vector de registros
        self.matriz_disponibilidad = [       # matriz: dias x horarios
            ["08:00", "09:00", "10:00", "11:00"],
            ["14:00", "15:00", "16:00", "17:00"]
        ]
        self.especialidades = ["Medicina general", "Pediatria", "Odontologia", "Ginecologia"]

    def registrar_paciente(self, paciente: Paciente) -> bool:
        if self.buscar_paciente(paciente.cedula) is not None:
            return False
        self.pacientes.append(paciente)
        return True

    def buscar_paciente(self, cedula: str) -> Optional[Paciente]:
        for paciente in self.pacientes:
            if paciente.cedula == cedula:
                return paciente
        return None

    def registrar_turno(self, cedula: str, fecha: str, hora: str, especialidad: str, medico: str) -> bool:
        if self.buscar_paciente(cedula) is None:
            return False
        if especialidad not in self.especialidades:
            return False
        if self.existe_turno(fecha, hora, medico):
            return False
        codigo = len(self.turnos) + 1
        self.turnos.append(Turno(codigo, cedula, fecha, hora, especialidad, medico))
        return True

    def existe_turno(self, fecha: str, hora: str, medico: str) -> bool:
        for turno in self.turnos:
            if turno.fecha == fecha and turno.hora == hora and turno.medico.lower() == medico.lower() and turno.estado != "Cancelado":
                return True
        return False

    def consultar_turnos_por_cedula(self, cedula: str) -> List[Turno]:
        return [turno for turno in self.turnos if turno.cedula_paciente == cedula]

    def visualizar_turnos(self) -> List[Turno]:
        return self.turnos

    def reporte_por_especialidad(self):
        reporte = {}
        for especialidad in self.especialidades:
            reporte[especialidad] = 0
        for turno in self.turnos:
            if turno.estado != "Cancelado":
                reporte[turno.especialidad] += 1
        return reporte

    def cancelar_turno(self, codigo: int) -> bool:
        for turno in self.turnos:
            if turno.codigo == codigo:
                turno.estado = "Cancelado"
                return True
        return False


def cargar_datos_demo(agenda: AgendaClinica):
    agenda.registrar_paciente(Paciente("1723456789", "Ana Maria Lopez", 28, "0991112223"))
    agenda.registrar_paciente(Paciente("0912345678", "Carlos Perez Zambrano", 41, "0983334445"))
    agenda.registrar_paciente(Paciente("2309876543", "Lucia Torres Vega", 10, "0975556667"))
    agenda.registrar_turno("1723456789", "2026-06-24", "08:00", "Medicina general", "Dra. Rivera")
    agenda.registrar_turno("0912345678", "2026-06-24", "09:00", "Odontologia", "Dr. Molina")
    agenda.registrar_turno("2309876543", "2026-06-25", "10:00", "Pediatria", "Dra. Cedeño")


def mostrar_menu():
    print("\nSISTEMA DE AGENDA DE TURNOS - CLINICA")
    print("1. Registrar paciente")
    print("2. Registrar turno")
    print("3. Consultar paciente por cedula")
    print("4. Visualizar todos los turnos")
    print("5. Reporte por especialidad")
    print("6. Cancelar turno")
    print("7. Salir")


def main():
    agenda = AgendaClinica()
    cargar_datos_demo(agenda)
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            cedula = input("Cedula: ")
            nombres = input("Nombres: ")
            edad = int(input("Edad: "))
            telefono = input("Telefono: ")
            ok = agenda.registrar_paciente(Paciente(cedula, nombres, edad, telefono))
            print("Paciente registrado correctamente." if ok else "Error: ya existe un paciente con esa cedula.")
        elif opcion == "2":
            cedula = input("Cedula del paciente: ")
            fecha = input("Fecha AAAA-MM-DD: ")
            hora = input("Hora HH:MM: ")
            especialidad = input("Especialidad: ")
            medico = input("Medico: ")
            ok = agenda.registrar_turno(cedula, fecha, hora, especialidad, medico)
            print("Turno registrado correctamente." if ok else "Error: paciente inexistente, especialidad invalida o turno ocupado.")
        elif opcion == "3":
            cedula = input("Cedula a consultar: ")
            paciente = agenda.buscar_paciente(cedula)
            if paciente:
                print(f"Paciente: {paciente.nombres} | Edad: {paciente.edad} | Telefono: {paciente.telefono}")
                for turno in agenda.consultar_turnos_por_cedula(cedula):
                    print(f"Turno {turno.codigo}: {turno.fecha} {turno.hora} - {turno.especialidad} - {turno.medico} - {turno.estado}")
            else:
                print("No se encontro el paciente.")
        elif opcion == "4":
            print("\nLISTADO DE TURNOS")
            for turno in agenda.visualizar_turnos():
                paciente = agenda.buscar_paciente(turno.cedula_paciente)
                nombre = paciente.nombres if paciente else "Sin datos"
                print(f"{turno.codigo}. {nombre} | {turno.fecha} | {turno.hora} | {turno.especialidad} | {turno.medico} | {turno.estado}")
        elif opcion == "5":
            print("\nREPORTE POR ESPECIALIDAD")
            for especialidad, total in agenda.reporte_por_especialidad().items():
                print(f"{especialidad}: {total} turno(s)")
        elif opcion == "6":
            codigo = int(input("Codigo de turno a cancelar: "))
            print("Turno cancelado." if agenda.cancelar_turno(codigo) else "No existe el turno.")
        elif opcion == "7":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    main()
