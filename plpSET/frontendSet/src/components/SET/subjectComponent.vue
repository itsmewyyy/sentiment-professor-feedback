<script setup lang="ts">
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardTitle,
  CardHeader,
  CardDescription,
  CardFooter,
} from "@/components/ui/card";
import { CircleCheckBig } from "lucide-vue-next";
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

// Define interfaces
interface ProfessorInfo {
  surname: string;
  first_name: string;
}

interface SubjectName {
  subject_code: string;
  subject_desc: string;
}

interface Subject {
  student_enrolled_subj_id: string;
  prof_subj_id: string;
  prof_info: ProfessorInfo;
  subj_name: SubjectName;
  is_evaluated: boolean;
}

interface EnrolledSubject {
  student_id: string;
  section: string;
  subjects: Subject[];
}

const enrolledSubjects = ref<EnrolledSubject[]>([]);
const router = useRouter();

// Fetch student's subjects from API
const fetchSubjects = async () => {
  try {
    const student_id = localStorage.getItem("student_id");
    const year_sem = localStorage.getItem("current_year_sem");

    const response = await axios.get<Subject[]>(
      `https://sentiment-professor-feedback-1.onrender.com/api/enrolled_subjs/${student_id}`
    );

    // Filter subjects by current year_sem
    const filteredSubjects = response.data.filter((subject) => {
      const subjectYearSem = subject.prof_subj_id.split("_")[0];
      return subjectYearSem === year_sem;
    });

    // Assign filtered subjects to enrolledSubjects
    enrolledSubjects.value = [
      { student_id, section: "", subjects: filteredSubjects },
    ];
    console.log("Filtered API response:", filteredSubjects);
  } catch (error) {
    console.error("Error fetching subjects:", error);
  }
};

function evaluateSubject(subject: Subject) {
  localStorage.setItem(
    "student_enrolled_subj_id",
    subject.student_enrolled_subj_id
  );
  router.push("/evaluation");
}

onMounted(() => {
  fetchSubjects();
});
</script>

<template>
  <div
    v-for="(enrolledSubj, enrolledSubjIndex) in enrolledSubjects"
    :key="enrolledSubjIndex"
    class="flex flex-wrap w-full sm:w-fit"
  >
    <div
      v-for="(subject, subjectIndex) in enrolledSubj.subjects"
      :key="subjectIndex"
      :id="`${subject.student_enrolled_subj_id}`"
      class="pb-4 sm:pb-6 lg:pb-8 pl-4 sm:pl-6 lg:pl-8 w-full sm:w-1/2 lg:w-1/3"
    >
      <Card
        class="w-full sm:w-80 h-48 sm:h-52 relative rounded-lg border border-black/15"
      >
        <div
          class="absolute top-0 left-0 w-full h-1/3 sm:h-1/2 bg-yellow-100/80 rounded-t-lg"
        ></div>
        <div class="relative h-full flex flex-col">
          <CardHeader>
            <CardTitle class="text-sm sm:text-base font-medium">
              {{ subject.subj_name.subject_desc }}
            </CardTitle>
            <CardDescription class="text-xs sm:text-sm text-gray-600">
              {{ subject.prof_info.first_name }} {{ subject.prof_info.surname }}
            </CardDescription>
          </CardHeader>
          <CardFooter class="flex justify-center mt-auto">
            <Button
              v-if="!subject.is_evaluated"
              class="bg-plpgreen-200 hover:bg-plpgreen-400 w-3/4 sm:w-1/2 text-xs sm:text-sm font-medium"
              @click="evaluateSubject(subject)"
            >
              Evaluate
            </Button>

            <div
              v-else
              class="font-medium flex space-x-1 items-center mb-2.5 cursor-not-allowed"
            >
              <p class="text-plpgreen-400 text-xs sm:text-sm">Evaluated</p>
              <CircleCheckBig class="w-4 h-4 sm:w-5 sm:h-5" color="#5F965E" />
            </div>
          </CardFooter>
          <Avatar
            class="absolute right-2 sm:right-4 top-1/2 transform -translate-y-1/2 w-10 sm:w-14 h-10 sm:h-14 rounded-full"
          >
            <AvatarImage
              src="https://plus.unsplash.com/premium_photo-1661942126259-fb08e7cce1e2?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            />
            <AvatarFallback>PLP</AvatarFallback>
          </Avatar>
        </div>
      </Card>
    </div>
  </div>
</template>
