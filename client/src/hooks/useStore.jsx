import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

const userStore = (set) => ({
  user: {},
  updateUser: (newUser) =>
    set(() => ({
      user: newUser,
    })),
  deleteUser: () =>
    set(() => ({
      user: null,
    })),
});
const useUserStore = create(
  devtools(
    persist(userStore, {
      name: "user",
    })
  )
);

export default useUserStore;
