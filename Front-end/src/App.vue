<template>
  <div id="app">
    <h1>Demo app</h1>
    <form @submit.prevent="addUser">
      <label for="name">Name:</label>
      <input type="text" id="name" v-model="name" required />

      <label for="email">Email:</label>
      <input type="email" id="email" v-model="email" required/>

      <button type="submit">Add User</button>
    </form>
    <hr>
    <div class="user" v-for="user in users" :key="user.id">
      <div v-if="user.editing">
        <form @submit.prevent="updateUser(user.id)">
          <label for="newName">New Name:</label>
          <input type="text" id="newName" v-model="user.newName" />

          <label for="newEmail">New Email:</label>
          <input type="email" id="newEmail" v-model="user.newEmail" />

          <button type="submit">Update</button>
          <button @click.prevent="user.editing = false">Cancel</button>
        </form>
      </div>
      <div v-else>
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <button @click="user.editing = true">Edit</button>
        <button @click="deleteUser(user.id)">Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "app",
  data() {
    return {
      users: [],
      name: "",
      email: "",
      baseApiUrl: "http://localhost:5000", // change this to your Flask API URL
    };
  },
  methods: {
    async addUser() {
      try {
        const response = await axios.post(`${this.baseApiUrl}/user`, {
          name: this.name,
          email: this.email,
        });
        this.users.push({ id: response.data.user_id, name: this.name, email: this.email });
        this.name = "";
        this.email = "";
      } catch (error) {
        console.error("Error adding user", error);
      }
    },
    async deleteUser(userId) {
      try {
        await axios.delete(`${this.baseApiUrl}/user/${userId}`);
        this.users = this.users.filter((user) => user.id !== userId);
      } catch (error) {
        console.error("Error deleting user", error);
      }
    },
    async updateUser(userId) {
      const user = this.users.find((u) => u.id === userId);
      try {
        await axios.put(`${this.baseApiUrl}/user/${userId}`, {
          name: user.newName,
          email: user.newEmail,
        });

        user.name = user.newName || user.name;
        user.email = user.newEmail || user.email;
        user.editing = false;
        user.newName = "";
        user.newEmail = "";
      } catch (error) {
        console.error("Error updating user", error);
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
