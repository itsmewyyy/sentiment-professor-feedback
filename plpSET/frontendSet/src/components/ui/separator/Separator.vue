<script setup>
import { computed } from "vue";
import { Separator } from "radix-vue";
import { cn } from "@/lib/utils";

const props = defineProps({
  orientation: { type: String, required: false },
  decorative: { type: Boolean, required: false },
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false },
  class: { type: null, required: false },
  label: { type: String, required: false },
});

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props;

  return delegated;
});
</script>

<template>
  <Separator
    v-bind="delegatedProps"
    :class="
      cn(
        'shrink-0 bg-slate-200 relative dark:bg-slate-800',
        props.orientation === 'vertical' ? 'w-px h-full' : 'h-px w-full',
        props.class
      )
    "
  >
    <span
      v-if="props.label"
      :class="
        cn(
          'text-xs text-slate-500 bg-white absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex justify-center items-center dark:text-slate-400 dark:bg-slate-950',
          props.orientation === 'vertical'
            ? 'w-[1px] px-1 py-2'
            : 'h-[1px] py-1 px-2'
        )
      "
      >{{ props.label }}</span
    >
  </Separator>
</template>
