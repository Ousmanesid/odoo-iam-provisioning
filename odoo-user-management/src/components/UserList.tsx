import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserList: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedUser, setSelectedUser] = useState<any>(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      // Note: Cette route n'existe pas dans l'API, on pourrait l'ajouter
      // Pour l'instant, on simule avec une liste vide ou on peut récupérer les groupes
      const response = await axios.get('/groups/');
      // Simulation de données utilisateurs pour la démo
      setUsers([]);
      setMessage({ type: 'success', text: 'Liste des utilisateurs chargée' });
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Erreur lors du chargement des utilisateurs'
      });
    } finally {
      setLoading(false);
    }
  };

  const getUserDetails = async (userId: number) => {
    try {
      const response = await axios.get(`/users/${userId}`);
      setSelectedUser(response.data);
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Erreur lors du chargement des détails utilisateur'
      });
    }
  };

  const getUserRoles = async (userId: number) => {
    try {
      const response = await axios.get(`/users/${userId}/roles`);
      return response.data.groups || [];
    } catch (error) {
      return [];
    }
  };

  const filteredUsers = users.filter(user =>
    user.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.login?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title mb-0">
          <i className="fas fa-list me-2"></i>
          Liste des utilisateurs
        </h3>
      </div>
      <div className="card-body">
        {/* Barre de recherche */}
        <div className="row mb-4">
          <div className="col-md-6">
            <div className="input-group">
              <span className="input-group-text">
                <i className="fas fa-search"></i>
              </span>
              <input
                type="text"
                className="form-control"
                placeholder="Rechercher un utilisateur..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="col-md-6 text-end">
            <button
              className="btn btn-outline-primary"
              onClick={fetchUsers}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                  Chargement...
                </>
              ) : (
                <>
                  <i className="fas fa-sync me-2"></i>
                  Actualiser
                </>
              )}
            </button>
          </div>
        </div>

        {/* Message */}
        {message && (
          <div className={`alert alert-${message.type === 'success' ? 'success' : 'danger'} mb-3`}>
            <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2`}></i>
            {message.text}
          </div>
        )}

        {/* Tableau des utilisateurs */}
        {loading ? (
          <div className="text-center py-4">
            <div className="spinner-border" role="status">
              <span className="visually-hidden">Chargement...</span>
            </div>
            <p className="mt-2">Chargement des utilisateurs...</p>
          </div>
        ) : (
          <>
            {filteredUsers.length === 0 ? (
              <div className="text-center py-4">
                <i className="fas fa-users fa-3x text-muted mb-3"></i>
                <h5 className="text-muted">Aucun utilisateur trouvé</h5>
                <p className="text-muted">
                  {searchTerm ? 'Aucun utilisateur ne correspond à votre recherche.' : 'La liste des utilisateurs est vide.'}
                </p>
                <div className="alert alert-info mt-3">
                  <i className="fas fa-info-circle me-2"></i>
                  <strong>Note :</strong> Pour afficher la liste des utilisateurs, vous devez d'abord implémenter 
                  l'endpoint <code>GET /users/</code> dans l'API FastAPI.
                </div>
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-striped table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nom</th>
                      <th>Login</th>
                      <th>Email</th>
                      <th>Statut</th>
                      <th>Groupes</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredUsers.map((user) => (
                      <tr key={user.id}>
                        <td>
                          <span className="badge bg-secondary">{user.id}</span>
                        </td>
                        <td>
                          <strong>{user.name}</strong>
                        </td>
                        <td>
                          <code>{user.login}</code>
                        </td>
                        <td>
                          <a href={`mailto:${user.email}`} className="text-decoration-none">
                            {user.email}
                          </a>
                        </td>
                        <td>
                          <span className={`badge ${user.active ? 'bg-success' : 'bg-danger'}`}>
                            {user.active ? 'Actif' : 'Inactif'}
                          </span>
                        </td>
                        <td>
                          <span className="badge bg-info">
                            {user.groups_id?.length || 0} groupe(s)
                          </span>
                        </td>
                        <td>
                          <div className="btn-group btn-group-sm" role="group">
                            <button
                              type="button"
                              className="btn btn-outline-primary"
                              onClick={() => getUserDetails(user.id)}
                              title="Voir détails"
                            >
                              <i className="fas fa-eye"></i>
                            </button>
                            <button
                              type="button"
                              className="btn btn-outline-success"
                              onClick={() => getUserRoles(user.id)}
                              title="Voir rôles"
                            >
                              <i className="fas fa-user-shield"></i>
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        )}

        {/* Modal pour détails utilisateur */}
        {selectedUser && (
          <div className="modal show d-block" tabIndex={-1} style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
            <div className="modal-dialog modal-lg">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">
                    <i className="fas fa-user me-2"></i>
                    Détails de l'utilisateur
                  </h5>
                  <button
                    type="button"
                    className="btn-close"
                    onClick={() => setSelectedUser(null)}
                  ></button>
                </div>
                <div className="modal-body">
                  <div className="row">
                    <div className="col-md-6">
                      <p><strong>ID :</strong> {selectedUser.id}</p>
                      <p><strong>Nom :</strong> {selectedUser.name}</p>
                      <p><strong>Login :</strong> {selectedUser.login}</p>
                      <p><strong>Email :</strong> {selectedUser.email}</p>
                    </div>
                    <div className="col-md-6">
                      <p><strong>Statut :</strong> 
                        <span className={`badge ms-2 ${selectedUser.active ? 'bg-success' : 'bg-danger'}`}>
                          {selectedUser.active ? 'Actif' : 'Inactif'}
                        </span>
                      </p>
                      <p><strong>Groupes :</strong> {selectedUser.groups_id?.length || 0}</p>
                    </div>
                  </div>
                  
                  {selectedUser.groups_id && selectedUser.groups_id.length > 0 && (
                    <div className="mt-3">
                      <h6>Groupes assignés :</h6>
                      <div className="d-flex flex-wrap gap-2">
                        {selectedUser.groups_id.map((groupId: number) => (
                          <span key={groupId} className="badge bg-primary">
                            Groupe ID: {groupId}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setSelectedUser(null)}
                  >
                    Fermer
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Statistiques */}
        <div className="row mt-4">
          <div className="col-md-3">
            <div className="card bg-primary text-white">
              <div className="card-body text-center">
                <h5 className="card-title">Total Utilisateurs</h5>
                <h2 className="card-text">{users.length}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-success text-white">
              <div className="card-body text-center">
                <h5 className="card-title">Utilisateurs Actifs</h5>
                <h2 className="card-text">{users.filter(u => u.active).length}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-warning text-white">
              <div className="card-body text-center">
                <h5 className="card-title">Utilisateurs Inactifs</h5>
                <h2 className="card-text">{users.filter(u => !u.active).length}</h2>
              </div>
            </div>
          </div>
          <div className="col-md-3">
            <div className="card bg-info text-white">
              <div className="card-body text-center">
                <h5 className="card-title">Résultats Filtrés</h5>
                <h2 className="card-text">{filteredUsers.length}</h2>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserList; 