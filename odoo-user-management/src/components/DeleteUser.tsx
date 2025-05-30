import React, { useState } from 'react';
import axios from 'axios';

interface DeleteUserProps {
  onUserDeleted: () => void;
}

const DeleteUser: React.FC<DeleteUserProps> = ({ onUserDeleted }) => {
  const [userId, setUserId] = useState('');
  const [userInfo, setUserInfo] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [searchLoading, setSearchLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);

  const searchUser = async () => {
    if (!userId.trim()) {
      setMessage({ type: 'error', text: 'Veuillez saisir un ID utilisateur' });
      return;
    }

    setSearchLoading(true);
    setMessage(null);
    setUserInfo(null);

    try {
      const response = await axios.get(`/users/${userId}`);
      setUserInfo(response.data);
      setMessage({ type: 'success', text: 'Utilisateur trouvé' });
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Utilisateur non trouvé'
      });
    } finally {
      setSearchLoading(false);
    }
  };

  const handleDelete = async () => {
    setLoading(true);
    setMessage(null);

    try {
      const response = await axios.delete(`/users/${userId}`);
      setMessage({
        type: 'success',
        text: response.data.message || 'Utilisateur supprimé avec succès'
      });

      // Reset form
      setUserId('');
      setUserInfo(null);
      setShowConfirmDialog(false);
      onUserDeleted();
    } catch (error: any) {
      setMessage({
        type: 'error',
        text: error.response?.data?.detail || 'Erreur lors de la suppression'
      });
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setUserId('');
    setUserInfo(null);
    setMessage(null);
    setShowConfirmDialog(false);
  };

  return (
    <div className="card">
      <div className="card-header bg-danger text-white">
        <h3 className="card-title mb-0">
          <i className="fas fa-user-times me-2"></i>
          Supprimer un utilisateur
        </h3>
      </div>
      <div className="card-body">
        <div className="alert alert-warning">
          <i className="fas fa-exclamation-triangle me-2"></i>
          <strong>Attention :</strong> La suppression d'un utilisateur est irréversible. 
          Assurez-vous que cette action est nécessaire.
        </div>

        {/* Recherche d'utilisateur */}
        <div className="row mb-4">
          <div className="col-12">
            <h5 className="text-primary border-bottom pb-2">Rechercher l'utilisateur à supprimer</h5>
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
                  <p><strong>Groupes :</strong> {userInfo.groups_id?.length || 0} groupe(s)</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Confirmation de suppression */}
        {userInfo && (
          <div className="row mb-4">
            <div className="col-12">
              <h5 className="text-danger border-bottom pb-2">Confirmation de suppression</h5>
              <div className="form-check mb-3">
                <input
                  className="form-check-input"
                  type="checkbox"
                  id="confirmDelete"
                  checked={showConfirmDialog}
                  onChange={(e) => setShowConfirmDialog(e.target.checked)}
                />
                <label className="form-check-label text-danger" htmlFor="confirmDelete">
                  <strong>Je confirme vouloir supprimer définitivement cet utilisateur</strong>
                </label>
              </div>
            </div>
          </div>
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
              className="btn btn-danger"
              onClick={handleDelete}
              disabled={!showConfirmDialog || loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                  Suppression...
                </>
              ) : (
                <>
                  <i className="fas fa-trash me-2"></i>
                  Supprimer définitivement
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default DeleteUser; 