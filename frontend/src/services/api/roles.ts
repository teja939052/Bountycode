import { requestWithRetry as request } from "./request.ts";

export const rolesApi = {
  // List all roles
  listRoles() {
    return request("/api/v1/roles/");
  },

  // Get a role's full package
  getRole(roleId: string) {
    return request(`/api/v1/roles/${roleId}`);
  },

  // Get all content for a role
  getRoleContent(roleId: string) {
    return request(`/api/v1/roles/${roleId}/content`);
  },

  // Get exercises for a role
  getExercises(roleId: string) {
    return request(`/api/v1/roles/${roleId}/exercises`);
  },

  // Get quizzes for a role
  getQuizzes(roleId: string) {
    return request(`/api/v1/roles/${roleId}/quizzes`);
  },

  // Get coding challenges for a role
  getChallenges(roleId: string) {
    return request(`/api/v1/roles/${roleId}/challenges`);
  },

  // Get practice sets for a role
  getPracticeSets(roleId: string) {
    return request(`/api/v1/roles/${roleId}/practice-sets`);
  },

  // Get a specific exercise
  getExercise(exerciseId: string) {
    return request(`/api/v1/roles/exercise/${exerciseId}`);
  },

  // Get a specific challenge
  getChallenge(challengeId: string) {
    return request(`/api/v1/roles/challenge/${challengeId}`);
  },

  // Get a specific quiz
  getQuiz(quizId: string) {
    return request(`/api/v1/roles/quiz/${quizId}`);
  },
};
