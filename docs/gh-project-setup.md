---
scope: How to set up and decorate a week's GitHub Project board (user projects of benjohnbill)
authority: Procedure. The week CLAUDE.md and the jungle-week-init skill point here
decided: 2026-11-13 — first used on project 7 (Week 11-12: AI 함께하기). He asked to reuse it each week
read_when: creating a week board, or changing a board's fields, views, README, or dates
---

# GitHub Project setup

How-to. The reference board is project 7:
https://github.com/users/benjohnbill/projects/7

## Target state

| Part | Setting |
|---|---|
| `Status` options | `Todo` GRAY "아직 시작하지 않은 일", `In Progress` YELLOW "지금 손대고 있는 일", `Done` GREEN "끝난 일" |
| Repository field (team week) | Single select `레포`, one option for each team repository, each with its own color and a one-line description |
| Date fields | `시작일` and `마감일` (type DATE) |
| View 1 | `전체 표`: Table, Group by `레포` |
| View 2 | `보드`: Board, columns `Status`, Group by (swimlanes) `레포`. Card fields add `Labels` and `레포` |
| View 3 | `로드맵`: Roadmap, start `시작일`, target `마감일`, Group by `레포`, zoom Month |
| Period items | One Draft item for each project period and one for the presentation, with `시작일` and `마감일` set |
| README and short description | Team-facing Korean text: the repositories table, how to read the views, a pointer to each repository's `CONVENTION.md` |

In a solo week, there is no `레포` field. Use the same views without the group.

## Which tool does which part

| Part | Tool |
|---|---|
| Fields, options, README, description, items, dates | `gh` CLI and `gh api graphql` |
| Views: create, rename, layout, group, card fields, roadmap date fields | Aside agent: `aside exec "<task>"` |

The GraphQL API has no mutation for views. In `aside repl`, clicks on GitHub
Primer menus do not open them (2026-11-13). `aside exec` works. Read
`~/.claude/docs/tool-guides/aside-browser.md` before you use Aside.

## Steps

Look up IDs every time. Never cache them.

1. Find the project number: `gh project list --owner benjohnbill`.
2. Get the field and option IDs:

   ```
   gh api graphql -f query='{user(login:"benjohnbill"){projectV2(number:N){id fields(first:30){nodes{... on ProjectV2SingleSelectField{id name options{id name color description}}}}}}}'
   ```

3. Take a snapshot of the item values before you change a field (see
   "Safety check").
4. Change option colors and descriptions with `updateProjectV2Field`.
   Send the `id` of each existing option. If you omit the `id`, GitHub makes
   new options, and every item loses its value for that field.

   ```
   mutation{updateProjectV2Field(input:{fieldId:"<field id>",singleSelectOptions:[
     {id:"<option id>",name:"Todo",color:GRAY,description:"아직 시작하지 않은 일"}, ...]}){projectV2Field{... on ProjectV2SingleSelectField{options{id name color}}}}}
   ```

5. Add the date fields:
   `gh project field-create N --owner benjohnbill --name 시작일 --data-type DATE`, then the same for `마감일`.
6. Write the README in a file, show it to him, then apply it:
   `gh project edit N --owner benjohnbill --readme "$(cat <file>)" --description "<one line>"`.
   The board is public and teammates read it. Never put the personal layer
   (week `CLAUDE.md`, `product-plan.md`) or a milestone answer in it.
7. Set the views with one `aside exec` task for each view. In the task, name
   the exact settings, say "save the view", and say "do not change anything
   else". Ask for the final state in the report.
8. Add period items with `gh project item-create`, then set `시작일`,
   `마감일`, `Status`, and `레포` with `gh project item-edit`. Ask him for the
   dates. Do not put a whole-period date on a milestone item.

## Safety check

Run this before and after each change, and `diff` the two outputs. The diff
must be empty, except for items that you added on purpose.

```
gh api graphql -f query='{user(login:"benjohnbill"){projectV2(number:N){items(first:100){nodes{id content{...on Issue{title}...on PullRequest{title}...on DraftIssue{title}} fieldValues(first:20){nodes{...on ProjectV2ItemFieldSingleSelectValue{optionId field{...on ProjectV2SingleSelectField{name}}}}}}}}}}' \
  | jq -S '[.data.user.projectV2.items.nodes[]|{id,t:.content.title,v:[.fieldValues.nodes[]|select(.optionId)|{f:.field.name,o:.optionId}]|sort_by(.f)}]|sort_by(.id)'
```

Check the views with the `views{nodes{number name layout groupByFields ...}}`
query. The API does not show the roadmap date fields. For those, use the Aside
report and ask him to look at the page.

## Known traps

- `gh project item-list --format json` breaks a Korean field name in the JSON
  key. Read field values through `gh api graphql`.
- The `Slice by` panel stays on a view after you add swimlanes. If both use
  `레포`, the view shows the same split twice. Ask him which one to keep.
