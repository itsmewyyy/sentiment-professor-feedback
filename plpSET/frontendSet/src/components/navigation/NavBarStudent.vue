<template>
  <div
    class="flex justify-between items-center w-full bg-white h-16 border-b border-black/25 px-4 z-10 top-0 fixed"
  >
    <!-- Left Section: Logo and Text -->
    <RouterLink to="/StudentDashboard">
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
      <!-- Calendar Icon with HoverCard -->
      <HoverCard>
        <HoverCardTrigger as-child>
          <Button variant="link">
            <Clock color="#2e5244" stroke-width="2" size="18" />
          </Button>
        </HoverCardTrigger>
        <HoverCardContent class="w-80 mr-20">
          <div class="flex justify-between space-x-4">
            <Avatar class="w-9 h-9">
              <AvatarImage src="https://github.com/vuejs.png" />
              <AvatarFallback>VC</AvatarFallback>
            </Avatar>
            <div class="space-y-1">
              <h4 class="text-sm font-semibold">@vuejs</h4>
              <p class="text-sm">
                Progressive JavaScript framework for building modern web
                interfaces.
              </p>
              <div class="flex items-center pt-2">
                <CalendarDays class="mr-2 h-4 w-4 opacity-70" />
                <span class="text-xs text-muted-foreground">
                  Joined January 2014
                </span>
              </div>
            </div>
          </div>
        </HoverCardContent>
      </HoverCard>

      <!-- Avatar (Frog Image) with Dropdown Menu -->
      <DropdownMenu>
        <DropdownMenuTrigger>
          <Avatar class="mt-2">
            <AvatarImage
              src="https://i.pinimg.com/564x/da/2a/20/da2a208141d20d42434ef3d4ae9c5d88.jpg"
            />
            <AvatarFallback>PLP</AvatarFallback>
          </Avatar>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-48 mr-7">
          <DropdownMenuLabel>
            <div class="flex flex-col space-y-0 line-clamp-2">
              <span class="font-medium">Gian Carlo Catalan</span>
              <span class="text-gray-500 italic text-xs">21-00444</span>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator class="bg-plpgreen-100 border-0.5" />
          <RouterLink to="/StudentProfile">
            <DropdownMenuItem>
              <div class="flex items-center space-x-2 cursor-pointer w-full">
                <User size="16" />
                <span class="text-sm">Profile</span>
              </div></DropdownMenuItem
            >
          </RouterLink>
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
import { User } from "lucide-vue-next";
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
import { CalendarDays, Clock, LogOut } from "lucide-vue-next";
import axios from "axios";
import { useAuthStore } from "@/store/student";
import { useRouter } from "vue-router";

const router = useRouter();

const logout = async () => {
  const authAdminLogin = useAuthStore();

  try {
    await authAdminLogin.logout();
    if (!authAdminLogin.isAuthenticated) {
      router.push("/");
    } else {
      console.error("Logout failed: User is still authenticated");
    }
  } catch (error) {
    console.error("Logout failed:", error);
  }
};
</script>
