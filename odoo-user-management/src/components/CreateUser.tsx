import React, { useState } from 'react';
import axios from 'axios';

interface CreateUserProps {
  onUserCreated: () => void;
}

interface UserAccount {
  login_name: string;
  other_ids: {
    id: string;
    guid: string;
    up_id: string;
    display_name: string;
  };
}

interface CreateUserRequest {
  user_account: UserAccount;
  name?: string;
  email?: string;
  password?: string;
  groups?: number[];
}

const CreateUser: React.FC<CreateUserProps> = ({ onUserCreated }) => {
  const [formData, setFormData] = useState<CreateUserRequest>({
    user_account: {
      login_name: '',
      other_ids: {
        id: '',
        guid: '',
        up_id: '',
        display_name: ''
      }
    },
    name: '',
    email: '',
    password: '',
    groups: []
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
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

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    
    if (name.startsWith('other_ids.')) {
      const field = name.split('.')[1];
      setFormData(prev => ({
        ...prev,
        user_account: {
          ...prev.user_account,
          other_ids: {
            ...prev.user_account.other_ids,
            [field]: value
          }
        }
      }));
    } else if (name === 'login_name') {
      setFormData(prev => ({
        ...prev,
        user_account: {
          ...prev.user_account,
          login_name: value
        }
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
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
    setLoading(true);
    setMessage(null);

    try {
      // Validation
      if (!formData.user_account.login_name.trim()) {
        throw new Error('Le nom de connexion est requis');
      }

      const requestData = {
        ...formData,
        groups: selectedGroups
      };

      const response = await axios.post('/users/', requestData);

      setMessage({
        type: 'success',
        text: `Utilisateur créé avec succès ! ID: ${response.data.user_id}${response.data.password !== '***' ? `, Mot de passe: ${response.data.password}` : ''}`
      });

      // Reset form
      setFormData({
        user_account: {
          login_name: '',
          other_ids: {
            id: '',
            guid: '',
            up_id: '',
            display_name: ''
          }
        },
        name: '',
        email: '',
        password: '',
        groups: []
      });
      setSelectedGroups([]);
      
      onUserCreated();
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || error.message || 'Erreur lors de la création de l\'utilisateur'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title mb-0">
          <i className="fas fa-user-plus me-2"></i>
          Créer un nouvel utilisateur
        </h3>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          {/* Informations de base */}
          <div className="row mb-4">
            <div className="col-12">
              <h5 className="text-primary border-bottom pb-2">Informations de base</h5>
            </div>
          </div>

          <div className="row mb-3">
            <div className="col-md-6">
              <label htmlFor="login_name" className="form-label">
                Nom de connexion <span className="text-danger">*</span>
              </label>
              <input
                type="text"
                className="form-control"
                id="login_name"
                name="login_name"
                value={formData.user_account.login_name}
                onChange={handleInputChange}
                required
                placeholder="john.doe@example.com"
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="john.doe@example.com"
              />
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
                placeholder="John Doe"
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="password" className="form-label">
                Mot de passe <small className="text-muted">(optionnel - généré automatiquement si vide)</small>
              </label>
              <input
                type="password"
                className="form-control"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Laissez vide pour génération automatique"
              />
            </div>
          </div>

          {/* Métadonnées Active Directory */}
          <div className="row mb-4">
            <div className="col-12">
              <h5 className="text-primary border-bottom pb-2">Métadonnées Active Directory</h5>
            </div>
          </div>

          <div className="row mb-3">
            <div className="col-md-6">
              <label htmlFor="other_ids.display_name" className="form-label">Nom d'affichage</label>
              <input
                type="text"
                className="form-control"
                id="other_ids.display_name"
                name="other_ids.display_name"
                value={formData.user_account.other_ids.display_name}
                onChange={handleInputChange}
                placeholder="John Doe"
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="other_ids.up_id" className="form-label">User Principal ID</label>
              <input
                type="text"
                className="form-control"
                id="other_ids.up_id"
                name="other_ids.up_id"
                value={formData.user_account.other_ids.up_id}
                onChange={handleInputChange}
                placeholder="123456"
              />
            </div>
          </div>

          <div className="row mb-3">
            <div className="col-md-6">
              <label htmlFor="other_ids.id" className="form-label">Distinguished Name (DN)</label>
              <input
                type="text"
                className="form-control"
                id="other_ids.id"
                name="other_ids.id"
                value={formData.user_account.other_ids.id}
                onChange={handleInputChange}
                placeholder="CN=John Doe,OU=Users,DC=example,DC=com"
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="other_ids.guid" className="form-label">GUID</label>
              <input
                type="text"
                className="form-control"
                id="other_ids.guid"
                name="other_ids.guid"
                value={formData.user_account.other_ids.guid}
                onChange={handleInputChange}
                placeholder="550e8400-e29b-41d4-a716-446655440000"
              />
            </div>
          </div>

          {/* Groupes */}
          <div className="row mb-4">
            <div className="col-12">
              <h5 className="text-primary border-bottom pb-2">Groupes et Permissions</h5>
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

          {/* Message */}
          {message && (
            <div className={`alert alert-${message.type === 'success' ? 'success' : 'danger'}`}>
              <i className={`fas fa-${message.type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2`}></i>
              {message.text}
            </div>
          )}

          {/* Boutons */}
          <div className="d-flex justify-content-between">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                setFormData({
                  user_account: {
                    login_name: '',
                    other_ids: {
                      id: '',
                      guid: '',
                      up_id: '',
                      display_name: ''
                    }
                  },
                  name: '',
                  email: '',
                  password: '',
                  groups: []
                });
                setSelectedGroups([]);
                setMessage(null);
              }}
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
                  Création en cours...
                </>
              ) : (
                <>
                  <i className="fas fa-user-plus me-2"></i>
                  Créer l'utilisateur
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateUser; 