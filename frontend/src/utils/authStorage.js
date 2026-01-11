/**
 * Utilitário para gerenciar armazenamento de autenticação
 * Permite escolher entre sessionStorage (sessão) e localStorage (permanente)
 */

export const authStorage = {
  // Define qual storage usar (session ou local)
  _storageType: 'session', // padrão: sessionStorage (limpa ao fechar)

  /**
   * Define o tipo de armazenamento
   * @param {string} type - 'session' ou 'local'
   */
  setStorageType(type) {
    this._storageType = type === 'local' ? 'local' : 'session'
  },

  /**
   * Obter o storage apropriado
   */
  _getStorage() {
    return this._storageType === 'local' ? localStorage : sessionStorage
  },

  /**
   * Definir token
   */
  setToken(token) {
    this._getStorage().setItem('authToken', token)
  },

  /**
   * Obter token
   */
  getToken() {
    return this._getStorage().getItem('authToken')
  },

  /**
   * Definir dados do usuário
   */
  setUser(userData) {
    this._getStorage().setItem('user', JSON.stringify(userData))
  },

  /**
   * Obter dados do usuário
   */
  getUser() {
    const user = this._getStorage().getItem('user')
    return user ? JSON.parse(user) : null
  },

  /**
   * Limpar tudo (logout)
   */
  clear() {
    // Limpar de ambos os storages para garantir
    localStorage.removeItem('authToken')
    localStorage.removeItem('user')
    sessionStorage.removeItem('authToken')
    sessionStorage.removeItem('user')
  },

  /**
   * Verificar se está autenticado
   */
  isAuthenticated() {
    return !!this.getToken()
  }
}
