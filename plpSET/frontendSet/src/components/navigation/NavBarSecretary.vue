<template>
  <div
    class="flex justify-between items-center w-full bg-white h-16 border-b border-black/25 px-4 z-10 top-0 fixed"
  >
    <!-- Left Section: Logo and Text -->
    <RouterLink to="/DeanDashboard">
      <div class="flex items-center space-x-2 cursor-pointer">
        <Avatar class="w-9 h-9">
          <AvatarImage
            src="https://plpasig.edu.ph/wp-content/uploads/2023/01/cropped-logo120.png"
          />
          <AvatarFallback>PLP</AvatarFallback>
        </Avatar>
        <p
          class="font-medium text-darks-200/80 transition-colors hover:text-darks-900 cursor-pointer text-sm"
        >
          Pamantasan ng Lungsod ng Pasig
        </p>
      </div>
    </RouterLink>

    <!-- Right Section: Calendar Icon with HoverCard and Avatar Dropdown -->
    <div class="flex items-center space-x-1">
      <!-- Avatar (Frog Image) with Dropdown Menu -->
      <DropdownMenu>
        <DropdownMenuTrigger>
          <Avatar class="w-9 h-9 mt-2">
            <AvatarImage
              src="https://i.pinimg.com/564x/da/2a/20/da2a208141d20d42434ef3d4ae9c5d88.jpg"
            />
            <AvatarFallback>PLP</AvatarFallback>
          </Avatar>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-50 mr-7">
          <DropdownMenuLabel>
            <div class="flex flex-col space-y-0 line-clamp-2">
              <span class="font-medium">{{ Admin }}</span>
              <span class="text-gray-500 italic text-xs">{{ College }}</span>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator class="bg-plpgreen-100 border-0.5" />
          <DropdownMenuItem>
            <div class="flex items-center space-x-2 cursor-pointer w-full">
              <User size="14" />
              <span class="text-sm">Profile</span>
            </div>
          </DropdownMenuItem>
          <DropdownMenuSeparator class="bg-plpgreen-100" />
          <DropdownMenuItem>
            <div
              class="flex items-center space-x-2 cursor-pointer w-full"
              @click="logout"
            >
              <LogOut size="14" />
              <span class="text-sm">Logout</span>
            </div>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </div>
</template>

<script setup>
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { CalendarDays, Clock, LogOut, User, Download } from "lucide-vue-next";

import { RouterLink } from "vue-router";
import axios from "axios";
import { useAuthStore } from "@/store/adminStore";
import { useRouter } from "vue-router";

const Admin = localStorage.getItem("admin_id");
const College = localStorage.getItem("college");

const router = useRouter();

const logout = async () => {
  const authAdminLogin = useAuthStore();

  try {
    await authAdminLogin.logout();
    router.push("/");
  } catch (error) {
    console.error("Logout failed:", error);
  }
};
</script>
