import React, { useState, useEffect } from "react";
import DataTable from "react-data-table-component";
import axios from "axios";
import { Modal, Button, Form, Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { logout, refreshToken, setAuthToken, isAuthenticated } from "../services/authService";

const UserDataTable = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [editForm, setEditForm] = useState({
    name: "",
    surname: "",
    control_number: "",
    email: "",
    tel: "",
    age: ""
  });
  const [alert, setAlert] = useState({ 
    show: false, 
    message: "", 
    variant: "success" 
  });
  const [currentUserId, setCurrentUserId] = useState(null);
  const navigate = useNavigate();

  const API_BASE_URL = "http://127.0.0.1:8000/users/api";

  useEffect(() => {
    const requestInterceptor = axios.interceptors.request.use(
      async (config) => {
        const token = localStorage.getItem("accessToken");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    const responseInterceptor = axios.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;
        
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          
          try {
            const newToken = await refreshToken();
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return axios(originalRequest);
          } catch (refreshError) {
            logout();
            navigate("/login");
            return Promise.reject(refreshError);
          }
        }
        
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.request.eject(requestInterceptor);
      axios.interceptors.response.eject(responseInterceptor);
    };
  }, [navigate]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (!isAuthenticated()) {
          navigate("/login");
          return;
        }

        setAuthToken(localStorage.getItem("accessToken"));

        const usersResponse = await axios.get(`${API_BASE_URL}/`);
        setData(usersResponse.data);

        try {
          const user = localStorage.getItem("user")
          const currentUserResponse = await axios.get(`${API_BASE_URL}/${user}/`);
          setCurrentUserId(currentUserResponse.data.id);
        } catch (error) {
          console.warn("No se pudo obtener usuario actual:", error);
          if (usersResponse.data.length > 0) {
            setCurrentUserId(usersResponse.data[0].id);
          }
        }
      } catch (error) {
        console.error("Error al cargar usuarios:", error);
        if (error.response?.status === 401) {
          navigate("/login");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate, API_BASE_URL]);

  const columns = [
    {
      name: "ID",
      selector: (row) => row.id,
      sortable: true,
      width: "80px"
    },
    {
      name: "Nombre",
      selector: (row) => row.name,
      sortable: true,
    },
    {
      name: "Email",
      selector: (row) => row.email,
      sortable: true,
    },
    {
      name: "Teléfono",
      selector: (row) => row.tel || "N/A",
    },
    {
      name: "Acciones",
      cell: (row) => (
        <div className="d-flex">
          <button
            className="btn btn-warning btn-sm me-2"
            onClick={() => handleEditClick(row)}
            disabled={row.id === currentUserId}
            title={row.id === currentUserId ? "No puedes editar tu propio usuario" : ""}
          >
            <i className="bi bi-pencil"></i> Editar
          </button>
          <button
            className="btn btn-danger btn-sm"
            onClick={() => handleDeleteClick(row)}
            disabled={row.id === currentUserId}
            title={row.id === currentUserId ? "No puedes borrar tu propio usuario" : ""}
          >
            <i className="bi bi-trash"></i> Eliminar
          </button>
        </div>
      ),
      ignoreRowClick: true,
      allowOverflow: true,
      button: true,
      width: "200px"
    },
  ];

  const handleDeleteClick = (user) => {
    setSelectedUser(user);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/${selectedUser.id}/`);
      setData(data.filter(user => user.id !== selectedUser.id));
      showAlert("Usuario eliminado correctamente", "success");
    } catch (error) {
      console.error("Error al eliminar:", error);
      showAlert(error.response?.data?.message || "Error al eliminar usuario", "danger");
    } finally {
      setShowDeleteModal(false);
    }
  };

  const handleEditClick = (user) => {
    setSelectedUser(user);
    setEditForm({
      name: user.name,
      surname: user.surname,
      control_number: user.control_number,
      email: user.email,
      tel: user.tel || "",
      age: user.age
    });
    setShowEditModal(true);
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setEditForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const confirmEdit = async () => {
    try {
      const response = await axios.put(
        `${API_BASE_URL}/${selectedUser.id}/`,
        editForm
      );
      
      setData(data.map(user => 
        user.id === selectedUser.id ? response.data : user
      ));
      
      showAlert("Usuario actualizado correctamente", "success");
      setShowEditModal(false);
    } catch (error) {
      console.error("Error al actualizar:", error);
      showAlert(error.response?.data?.message || "Error al actualizar usuario", "danger");
    }
  };

  const showAlert = (message, variant) => {
    setAlert({ show: true, message, variant });
    setTimeout(() => {
      setAlert(prev => ({ ...prev, show: false }));
    }, 5000);
  };

  return (
    <div className="p-3">
      <h2 className="mb-4">Gestión de Usuarios</h2>
      
      {alert.show && (
        <Alert 
          variant={alert.variant} 
          onClose={() => setAlert(prev => ({ ...prev, show: false }))} 
          dismissible
          className="mt-3"
        >
          {alert.message}
        </Alert>
      )}

      <DataTable
        columns={columns}
        data={data}
        progressPending={loading}
        pagination
        paginationPerPage={10}
        paginationRowsPerPageOptions={[5, 10, 15, 20]}
        highlightOnHover
        pointerOnHover
        noDataComponent={
          <div className="py-5 text-center">
            <h4>No hay usuarios registrados</h4>
          </div>
        }
        striped
        responsive
        className="border rounded"
      />

      {/* Modal de confirmación para eliminar */}
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirmar Eliminación</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          ¿Estás seguro que deseas eliminar al usuario <strong>{selectedUser?.name}</strong>?
          <br />
          <span className="text-danger">Esta acción no se puede deshacer.</span>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            Cancelar
          </Button>
          <Button variant="danger" onClick={confirmDelete}>
            <i className="bi bi-trash"></i> Eliminar
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Modal de edición */}
      <Modal show={showEditModal} onHide={() => setShowEditModal(false)} size="lg" centered>
        <Modal.Header closeButton>
          <Modal.Title>Editar Usuario: {selectedUser?.name}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Nombre </Form.Label>
              <Form.Control
                type="text"
                name="name"
                value={editForm.name}
                onChange={handleFormChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Apellidos </Form.Label>
              <Form.Control
                type="text"
                name="surname"
                value={editForm.surname}
                onChange={handleFormChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={editForm.email}
                onChange={handleFormChange}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Teléfono</Form.Label>
              <Form.Control
                type="tel"
                name="tel"
                value={editForm.tel}
                onChange={handleFormChange}
                placeholder="Opcional"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Matricula</Form.Label>
              <Form.Control
                type="control_number"
                name="control_number"
                value={editForm.control_number}
                onChange={handleFormChange}
                placeholder="Opcional"
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Edad</Form.Label>
              <Form.Control
                type="age"
                name="age"
                value={editForm.age}
                onChange={handleFormChange}
                placeholder="Opcional"
              />
            </Form.Group>

          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowEditModal(false)}>
            Cancelar
          </Button>
          <Button variant="primary" onClick={confirmEdit}>
            <i className="bi bi-save"></i> Guardar Cambios
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default UserDataTable;