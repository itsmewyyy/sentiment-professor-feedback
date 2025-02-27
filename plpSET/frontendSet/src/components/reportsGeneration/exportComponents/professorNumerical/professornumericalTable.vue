<template>
  <div class="flex justify-center p-2">
    <Table class="border text-sm">
      <TableHeader>
        <TableRow>
          <TableHead class="w-[40px] font-bold border-r p-2"
            >CATEGORY</TableHead
          >
          <TableHead class="w-[40px] font-bold border-r p-2"
            >Questionnaire</TableHead
          >
          <TableHead class="w-[100px] text-center font-bold p-2"
            >Average</TableHead
          >
        </TableRow>
      </TableHeader>
      <TableBody>
        <template
          v-for="(category, categoryIndex) in categories"
          :key="categoryIndex"
        >
          <TableRow class="bg-muted/50">
            <TableCell
              class="font-bold align-top p-2 border-r"
              :rowspan="category.questions.length + 1"
            >
              {{ category.category_desc }}
            </TableCell>
          </TableRow>
          <TableRow
            v-for="(question, questionIndex) in category.questions"
            :key="question.numerical_question_id"
          >
            <TableCell class="border-r p-2">{{ question.question }}</TableCell>
            <TableCell class="text-center p-2">
              {{ question.average !== null ? question.average : "N/A" }}
            </TableCell>
          </TableRow>
        </template>
      </TableBody>
    </Table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const categories = ref([]);

const props = defineProps({
  refreshChart: Boolean,
});

watch(
  () => props.refreshChart,
  () => {
    fetchCategoriesAndAverages();
  }
);

const fetchCategoriesAndAverages = async () => {
  const professorId = localStorage.getItem("professor");
  const yearsemIdentifier = localStorage.getItem("current_year_sem");

  if (!professorId || !yearsemIdentifier) {
    console.error(
      "Professor ID or year/semester identifier not found in localStorage."
    );
    return;
  }

  try {
    // Fetch categories and questions
    const categoriesResponse = await axios.get(
      "https://sentiment-professor-feedback-1.onrender.com/api/categories-and-questions/"
    );
    const allCategories = categoriesResponse.data;

    // Fetch professor ratings summary
    const ratingsResponse = await axios.get(
      "https://sentiment-professor-feedback-1.onrender.com/api/professor-ratings-summary/"
    );
    console.log(ratingsResponse);

    // Filter by year/semester and professor ID
    const professorData = ratingsResponse.data
      .find((item) => item.year_sem === yearsemIdentifier)
      ?.professors.find((professor) => professor.id === professorId);

    if (professorData) {
      categories.value = allCategories.map((category) => {
        const categorySummary =
          professorData.numerical_summary.category_avg.find(
            (avgCategory) =>
              avgCategory.category_desc === category.category_desc
          );

        return {
          category_desc: category.category_desc,
          questions: category.questions.map((question) => {
            const questionAvg = categorySummary?.question_avg.find(
              (avgQuestion) =>
                avgQuestion.question_id === question.numerical_question_id
            );

            return {
              numerical_question_id: question.numerical_question_id,
              question: question.question,
              average: questionAvg
                ? parseFloat(questionAvg.average.toFixed(2))
                : "N/A",
            };
          }),
        };
      });
    } else {
      console.warn(
        `No data found for professor ID: ${professorId} and year/semester: ${yearsemIdentifier}`
      );
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// Fetch data on component mount
onMounted(fetchCategoriesAndAverages);
</script>
