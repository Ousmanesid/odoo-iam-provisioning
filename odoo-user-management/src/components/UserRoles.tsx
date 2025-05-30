import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface UserRolesProps {
  onRolesChanged: () => void;
}

const UserRoles: React.FC<UserRolesProps> = ({ onRolesChanged }) => {
  const [userId, setUserId] = useState('');
  const [userInfo, setUserInfo] = useState<any>(null);
  const [userRoles, setUserRoles] = useState<any[]>([]);
  const [availableGroups, setAvailableGroups] = useState<any[]>([]);
  const [selectedGroupsToAdd, setSelectedGroupsToAdd] = useState<number[]>([]);
  const [selectedGroupsToRemove, setSelectedGroupsToRemove] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    try {
      const response = await axios.get('/groups/');
      setAvailableGroups(response.data.groups || []);
    } catch (error) {
      console.error('Erreur lors du chargement des groupes:', error);
    }
  };

  const searchUser = async () => {
    if (!userId.trim()) {
      setMessage({ type: 'error', text: 'Veuillez saisir un ID utilisateur' });
      return;
    }

    setSearchLoading(true);
    setMessage(null);

    try {
      // Récupérer les informations utilisateur
      const userResponse = await axios.get(`/users/${userId}`);
      setUserInfo(userResponse.data);

      // Récupérer les rôles utilisateur
      const rolesResponse = await axios.get(`/users/${userId}/roles`);
      setUserRoles(rolesResponse.data.groups || []);

      setMessage({ type: 'success', text: 'Utilisateur trouvé et rôles chargés' });
    } catch (error: any) {
      setUserInfo(null);
      setUserRoles([]);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Utilisateur non trouvé'
      });
    } finally {
      setSearchLoading(false);
    }
  };

  const handleAddRoles = async () => {
    if (selectedGroupsToAdd.length === 0) {
      setMessage({ type: 'error', text: 'Veuillez sélectionner au moins un groupe à ajouter' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.post(`/users/${userId}/roles`, {
        groups: selectedGroupsToAdd
      });

      setMessage({
        type: 'success',
        text: response.data.message || 'Rôles ajoutés avec succès'
      });

      // Recharger les rôles
      await searchUser();
      setSelectedGroupsToAdd([]);
      onRolesChanged();
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Erreur lors de l\'ajout des rôles'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveRoles = async () => {
    if (selectedGroupsToRemove.length === 0) {
      setMessage({ type: 'error', text: 'Veuillez sélectionner au moins un groupe à retirer' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.delete(`/users/${userId}/roles`, {
        data: { groups: selectedGroupsToRemove }
      });

      setMessage({
        type: 'success',
        text: response.data.message || 'Rôles retirés avec succès'
      });

      // Recharger les rôles
      await searchUser();
      setSelectedGroupsToRemove([]);
      onRolesChanged();
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Erreur lors du retrait des rôles'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGroupToAddChange = (groupId: number, isChecked: boolean) => {
    if (isChecked) {
      setSelectedGroupsToAdd(prev => [...prev, groupId]);
    } else {
      setSelectedGroupsToAdd(prev => prev.filter(id => id !== groupId));
    }
  };

  const handleGroupToRemoveChange = (groupId: number, isChecked: boolean) => {
    if (isChecked) {
      setSelectedGroupsToRemove(prev => [...prev, groupId]);
    } else {
      setSelectedGroupsToRemove(prev => prev.filter(id => id !== groupId));
    }
  };

  const resetForm = () => {
    setUserId('');
    setUserInfo(null);
    setUserRoles([]);
    setSelectedGroupsToAdd([]);
    setSelectedGroupsToRemove([]);
    setMessage(null);
  };

  const currentGroupIds = userRoles.map(role => role.id);
  const availableGroupsToAdd = availableGroups.filter(group => !currentGroupIds.includes(group.id));
  const availableGroupsToRemove = userRoles;

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title mb-0">
          <i className="fas fa-user-shield me-2"></i>
          Gestion des rôles utilisateur
        </h3>
      </div>
      <div className="card-body">
        {/* Recherche d'utilisateur */}
        <div className="row mb-4">
          <div className="col-12">
            <h5 className="text-primary border-bottom pb-2">Rechercher l'utilisateur</h5>
          </div>
        </div>

        <div className="row mb-4">
          <div className="col-md-8">
            <label htmlFor="userId" className="form-label">
              ID Utilisateur <span className="text-danger">*</span>
            </label>
            <input
              type="number"
              className="form-control"
              id="userId"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="Saisissez l'ID de l'utilisateur"
            />
          </div>
          <div className="col-md-4 d-flex align-items-end">
            <button
              type="button"
              className="btn btn-outline-primary w-100"
              onClick={searchUser}
              disabled={searchLoading}
            >
              {searchLoading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                  Recherche...
                </>
              ) : (
                <>
                  <i className="fas fa-search me-2"></i>
                  Rechercher
                </>
              )}
            </button>
          </div>
        </div>

        {/* Informations utilisateur */}
        {userInfo && (
          <div className="card mb-4">
            <div className="card-header">
              <h6 className="card-title mb-0">Informations de l'utilisateur</h6>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-6">
                  <p><strong>ID :</strong> {userInfo.id}</p>
                  <p><strong>Nom :</strong> {userInfo.name}</p>
                  <p><strong>Login :</strong> {userInfo.login}</p>
                </div>
                <div className="col-md-6">
                  <p><strong>Email :</strong> {userInfo.email}</p>
                  <p><strong>Actif :</strong> {userInfo.active ? 'Oui' : 'Non'}</p>
                  <p><strong>Rôles actuels :</strong> {userRoles.length} rôle(s)</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Rôles actuels */}
        {userRoles.length > 0 && (
          <div className="row mb-4">
            <div className="col-12">
              <h5 className="text-success border-bottom pb-2">Rôles actuels</h5>
              <div className="d-flex flex-wrap gap-2 mb-3">
                {userRoles.map((role) => (
                  <span key={role.id} className="badge bg-success fs-6">
                    {role.name}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {userInfo && (
          <>
            {/* Ajouter des rôles */}
            <div className="row mb-4">
              <div className="col-12">
                <h5 className="text-primary border-bottom pb-2">Ajouter des rôles</h5>
                {availableGroupsToAdd.length > 0 ? (
                  <div className="row">
                    {availableGroupsToAdd.map((group) => (
                      <div key={group.id} className="col-md-4 col-sm-6 mb-2">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            id={`add-group-${group.id}`}
                            checked={selectedGroupsToAdd.includes(group.id)}
                            onChange={(e) => handleGroupToAddChange(group.id, e.target.checked)}
                          />
                          <label className="form-check-label" htmlFor={`add-group-${group.id}`}>
                            <small>{group.name}</small>
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-muted">Aucun nouveau rôle disponible à ajouter.</p>
                )}
                
                {selectedGroupsToAdd.length > 0 && (
                  <button
                    type="button"
                    className="btn btn-success mt-2"
                    onClick={handleAddRoles}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Ajout en cours...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-plus me-2"></i>
                        Ajouter {selectedGroupsToAdd.length} rôle(s)
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>

            {/* Retirer des rôles */}
            <div className="row mb-4">
              <div className="col-12">
                <h5 className="text-danger border-bottom pb-2">Retirer des rôles</h5>
                {availableGroupsToRemove.length > 0 ? (
                  <div className="row">
                    {availableGroupsToRemove.map((role) => (
                      <div key={role.id} className="col-md-4 col-sm-6 mb-2">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            id={`remove-group-${role.id}`}
                            checked={selectedGroupsToRemove.includes(role.id)}
                            onChange={(e) => handleGroupToRemoveChange(role.id, e.target.checked)}
                          />
                          <label className="form-check-label" htmlFor={`remove-group-${role.id}`}>
                            <small className="text-danger">{role.name}</small>
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-muted">Aucun rôle à retirer.</p>
                )}

                {selectedGroupsToRemove.length > 0 && (
                  <button
                    type="button"
                    className="btn btn-danger mt-2"
                    onClick={handleRemoveRoles}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Retrait en cours...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-minus me-2"></i>
                        Retirer {selectedGroupsToRemove.length} rôle(s)
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          </>
        )}

        {/* Message */}
        {message && (
          <div className={`alert alert-${message.type === 'success' ? 'success' : 'danger'} mb-3`}>
            <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2`}></i>
            {message.text}
          </div>
        )}

        {/* Boutons */}
        <div className="d-flex justify-content-between">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={resetForm}
          >
            <i className="fas fa-undo me-2"></i>
            Réinitialiser
          </button>
          
          {userInfo && (
            <button
              type="button"
              className="btn btn-info"
              onClick={searchUser}
              disabled={searchLoading}
            >
              <i className="fas fa-sync me-2"></i>
              Actualiser les rôles
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserRoles; 