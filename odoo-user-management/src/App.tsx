import React, { useState } from 'react';
import CreateUser from './components/CreateUser';
import UpdateUser from './components/UpdateUser';
import DeleteUser from './components/DeleteUser';
import UserList from './components/UserList';
import UserRoles from './components/UserRoles';

function App() {
  const [activeTab, setActiveTab] = useState('create');
  const [refreshKey, setRefreshKey] = useState(0);

  const handleUserChange = () => {
    setRefreshKey(prev => prev + 1);
  };

  return (
    <div className="App">
      {/* Navigation */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container">
          <a className="navbar-brand" href="#">
            <i className="fas fa-users me-2"></i>
            Gestion des Utilisateurs Odoo
          </a>
        </div>
      </nav>

      <div className="container mt-4">
        {/* Tabs Navigation */}
        <ul className="nav nav-tabs mb-4">
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'create' ? 'active' : ''}`}
              onClick={() => setActiveTab('create')}
            >
              <i className="fas fa-user-plus me-2"></i>
              Créer un utilisateur
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'list' ? 'active' : ''}`}
              onClick={() => setActiveTab('list')}
            >
              <i className="fas fa-list me-2"></i>
              Liste des utilisateurs
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'update' ? 'active' : ''}`}
              onClick={() => setActiveTab('update')}
            >
              <i className="fas fa-user-edit me-2"></i>
              Modifier un utilisateur
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'roles' ? 'active' : ''}`}
              onClick={() => setActiveTab('roles')}
            >
              <i className="fas fa-user-shield me-2"></i>
              Gérer les rôles
            </button>
          </li>
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'delete' ? 'active' : ''}`}
              onClick={() => setActiveTab('delete')}
            >
              <i className="fas fa-user-times me-2"></i>
              Supprimer un utilisateur
            </button>
          </li>
        </ul>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'create' && (
            <div className="tab-pane fade show active">
              <CreateUser onUserCreated={handleUserChange} />
            </div>
          )}
          
          {activeTab === 'list' && (
            <div className="tab-pane fade show active">
              <UserList key={refreshKey} />
            </div>
          )}
          
          {activeTab === 'update' && (
            <div className="tab-pane fade show active">
              <UpdateUser onUserUpdated={handleUserChange} />
            </div>
          )}
          
          {activeTab === 'roles' && (
            <div className="tab-pane fade show active">
              <UserRoles onRolesChanged={handleUserChange} />
            </div>
          )}
          
          {activeTab === 'delete' && (
            <div className="tab-pane fade show active">
              <DeleteUser onUserDeleted={handleUserChange} />
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-light mt-5 py-4">
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <p className="text-muted mb-0">
                Système de provisionnement IAM pour Odoo
              </p>
            </div>
            <div className="col-md-6 text-end">
              <p className="text-muted mb-0">
                Développé avec React et FastAPI
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App; 