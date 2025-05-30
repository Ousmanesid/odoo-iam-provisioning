import React, { useState } from 'react';
import axios from 'axios';

interface UpdateUserProps {
  onUserUpdated: () => void;
}

interface UpdateUserRequest {
  name?: string;
  login?: string;
  email?: string;
  password?: string;
  groups?: number[];
}

const UpdateUser: React.FC<UpdateUserProps> = ({ onUserUpdated }) => {
  const [userId, setUserId] = useState('');
  const [formData, setFormData] = useState<UpdateUserRequest>({
    name: '',
    login: '',
    email: '',
    password: '',
    groups: []
  });

  const [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [userFound, setUserFound] = useState(false);
  const [availableGroups, setAvailableGroups] = useState<any[]>([]);
  const [selectedGroups, setSelectedGroups] = useState<number[]>([]);

  React.useEffect(() => {
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
      const response = await axios.get(`/users/${userId}`);
      const userData = response.data;

      setFormData({
        name: userData.name || '',
        login: userData.login || '',
        email: userData.email || '',
        password: '',
        groups: userData.groups_id || []
      });

      setSelectedGroups(userData.groups_id || []);
      setUserFound(true);
      setMessage({ type: 'success', text: 'Utilisateur trouvé et chargé' });
    } catch (error: any) {
      setUserFound(false);
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Utilisateur non trouvé'
      });
    } finally {
      setSearchLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleGroupChange = (groupId: number, isChecked: boolean) => {
    if (isChecked) {
      setSelectedGroups(prev => [...prev, groupId]);
    } else {
      setSelectedGroups(prev => prev.filter(id => id !== groupId));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userFound) {
      setMessage({ type: 'error', text: 'Veuillez d\'abord rechercher un utilisateur' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const updateData: UpdateUserRequest = {};
      
      // N'inclure que les champs modifiés
      if (formData.name?.trim()) updateData.name = formData.name.trim();
      if (formData.login?.trim()) updateData.login = formData.login.trim();
      if (formData.email?.trim()) updateData.email = formData.email.trim();
      if (formData.password?.trim()) updateData.password = formData.password.trim();
      if (selectedGroups.length > 0) updateData.groups = selectedGroups;

      const response = await axios.put(`/users/${userId}`, updateData);

      setMessage({
        type: 'success',
        text: response.data.message || 'Utilisateur mis à jour avec succès'
      });

      onUserUpdated();
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Erreur lors de la mise à jour'
      });
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setUserId('');
    setFormData({
      name: '',
      login: '',
      email: '',
      password: '',
      groups: []
    });
    setSelectedGroups([]);
    setUserFound(false);
    setMessage(null);
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title mb-0">
          <i className="fas fa-user-edit me-2"></i>
          Modifier un utilisateur existant
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

        {/* Formulaire de modification */}
        {userFound && (
          <form onSubmit={handleSubmit}>
            <div className="row mb-4">
              <div className="col-12">
                <h5 className="text-primary border-bottom pb-2">Modifier les informations</h5>
                <small className="text-muted">Laissez les champs vides pour ne pas les modifier</small>
              </div>
            </div>

            <div className="row mb-3">
              <div className="col-md-6">
                <label htmlFor="name" className="form-label">Nom complet</label>
                <input
                  type="text"
                  className="form-control"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Nouveau nom complet"
                />
              </div>
              <div className="col-md-6">
                <label htmlFor="login" className="form-label">Login</label>
                <input
                  type="text"
                  className="form-control"
                  id="login"
                  name="login"
                  value={formData.login}
                  onChange={handleInputChange}
                  placeholder="Nouveau login"
                />
              </div>
            </div>

            <div className="row mb-3">
              <div className="col-md-6">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  className="form-control"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  placeholder="Nouvel email"
                />
              </div>
              <div className="col-md-6">
                <label htmlFor="password" className="form-label">
                  Nouveau mot de passe
                </label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder="Nouveau mot de passe"
                />
              </div>
            </div>

            {/* Groupes */}
            <div className="row mb-4">
              <div className="col-12">
                <h5 className="text-primary border-bottom pb-2">Groupes</h5>
                <div className="row">
                  {availableGroups.length > 0 ? (
                    availableGroups.slice(0, 12).map((group) => (
                      <div key={group.id} className="col-md-4 col-sm-6 mb-2">
                        <div className="form-check">
                          <input
                            className="form-check-input"
                            type="checkbox"
                            id={`group-${group.id}`}
                            checked={selectedGroups.includes(group.id)}
                            onChange={(e) => handleGroupChange(group.id, e.target.checked)}
                          />
                          <label className="form-check-label" htmlFor={`group-${group.id}`}>
                            <small>{group.name}</small>
                          </label>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="col-12">
                      <p className="text-muted">Chargement des groupes...</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

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
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                    Mise à jour...
                  </>
                ) : (
                  <>
                    <i className="fas fa-save me-2"></i>
                    Mettre à jour
                  </>
                )}
              </button>
            </div>
          </form>
        )}

        {/* Message */}
        {message && (
          <div className={`alert alert-${message.type === 'success' ? 'success' : 'danger'} mt-3`}>
            <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2`}></i>
            {message.text}
          </div>
        )}
      </div>
    </div>
  );
};

export default UpdateUser; 