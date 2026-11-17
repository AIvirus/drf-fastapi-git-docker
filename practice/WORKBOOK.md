# Practice Workbook — Day 3

Use this **after** the lessons, for revision. Answer in your own words first, then check [ANSWERS.md](ANSWERS.md).
The lesson number in brackets tells you where to look if you are stuck.

## Section A — REST APIs (Lesson 01)
1. What is an API? Explain it with your own real-life example.
2. How is an API different from the website you built on Day 2?
3. What does REST mean, and name four REST ideas.
4. Why should REST URLs use nouns (`/articles/`) and not verbs (`/getArticles`)?
5. Which HTTP method is used to: create, list, read one, replace, change part, delete?
6. What do 200, 201, 204, 400, 401, 403, 404, 405, 422 and 500 mean?
7. What is JSON? Write a JSON object for a student with a name, age, a list of subjects and `is_active`.
8. What does "stateless" mean for a REST API?
9. What is a query parameter? Give an example URL.
10. *(Lesson 01, Try it yourself 3 + 4)* Write the method + URL + expected success code for a library app: list all books; add a book; change only the price of book 12; remove book 12; only books by author 5.
11. What is the `Content-Type` header for JSON?

## Section B — Django REST Framework basics (Lessons 03–06)
12. What is Django REST Framework and what does it add to Django?
13. `Response` vs `HttpResponse` — what's the difference?
14. What is the browsable API? Why does the browser get HTML but Postman gets JSON?
15. What is a serializer? What does it do in each direction?
16. `Serializer` vs `ModelSerializer`?
17. What do `serializer.is_valid()`, `.errors`, `.validated_data` and `.save()` do?
18. How do you write validation for one field? For several fields together?
19. What does `ReadOnlyField(source="author.username")` do, and why is it important for security?
20. What does `write_only=True` do? Give an example where you need it.
21. `PrimaryKeyRelatedField`, `StringRelatedField` and a nested serializer — what does each one show?
22. What does `@api_view(["GET", "POST"])` do?
23. Name two differences between `@api_view` functions and `APIView` classes.
24. What is a generic view? Name three and the methods they allow.
25. What is `perform_create()` used for?
26. What is a ViewSet? List the six actions of a `ModelViewSet`.
27. What does a router do? What extra page does `DefaultRouter` give you?
28. What does `get_queryset()` decide, and why does a draft return 404 for another user?
29. What is pagination and why is it needed?
30. What does `@action(detail=False)` create? And `detail=True`?
31. What do `select_related` and `prefetch_related` fix?
32. PUT vs PATCH?

## Section C — Authentication and permissions (Lessons 07–08)
33. Authentication vs authorization.
34. 401 vs 403.
35. Name four DRF authentication classes and when each is used.
36. Name five DRF permission classes.
37. `has_permission` vs `has_object_permission`.
38. What are "safe methods"?
39. Why did `ArticleViewSet` need `IsAuthenticatedOrReadOnly` **and** `IsAuthorOrReadOnly`?
40. How does a client send a DRF Token? A JWT?
41. Why must you use `create_user()` and not `User.objects.create()` to register a user?
42. What are the three parts of a JWT?
43. Is the JWT payload secret? Can it be changed by the client? Explain.
44. Access token vs refresh token.
45. Two problems of simple DRF tokens that JWT solves.
46. Why is the `SECRET_KEY` so important when you use JWT?

## Section D — Testing APIs (Lesson 09)
47. What is a Postman collection? An environment? A variable?
48. What does this Postman script do: `pm.environment.set("access", pm.response.json().access);`?
49. Why run a whole collection with the Collection Runner?
50. `APITestCase` — which database does it use, and why is that good?
51. `force_authenticate()` vs `credentials()` — when do you use each?
52. Why must you pass `format="json"` in `self.client.post(...)`?
53. What are the "3 A's" of a test?

## Section E — FastAPI (Lessons 10–13)
54. What is FastAPI? Name three advantages.
55. Give two situations where you'd choose Django + DRF, and two where you'd choose FastAPI.
56. What is uvicorn? What does `uvicorn main:app --reload` mean?
57. What are `/docs`, `/redoc` and `/openapi.json`?
58. What is OpenAPI, and why is it useful for AI agents?
59. How does FastAPI know whether an argument is a path parameter, a query parameter or the body?
60. How do you make a query parameter optional?
61. What is Pydantic? What happens when the data is invalid?
62. What does `Field(min_length=3, ge=1, le=5)` mean?
63. What does `response_model` do? Give an example where it protects data.
64. How do you return a 404 in FastAPI?
65. Why do we have `TaskCreate`, `TaskUpdate` and `TaskRead` instead of one model?
66. What does `model_dump(exclude_unset=True)` do and why does PATCH need it?
67. Why must `/tasks/stats` be defined before `/tasks/{task_id}`?
68. What is SQLModel? What does `table=True` mean?
69. Explain `session.add()`, `commit()` and `refresh()`.
70. What is `Depends(get_session)` and why is it useful in tests?
71. Is `SQLModel.metadata.create_all()` a full migration tool? What do real projects use?
72. `def` vs `async def` in FastAPI — which should a beginner use and why?

## Section F — Git (Lesson 14)
73. What is version control? Name three problems it solves.
74. Git vs GitHub.
75. Explain the working directory, staging area and repository.
76. What do `git init`, `git status`, `git add`, `git commit`, `git log` and `git diff` do?
77. Why do we need a staging area?
78. What is a commit? What information does it contain?
79. Write three good commit messages and say what makes them good.
80. What is `.gitignore`? Name four things that should be in it, and why.
81. You committed a secret by accident. Is deleting the file in a new commit enough? What must you do?
82. How do you undo unstaged changes to a file? How do you unstage a file?

## Section G — GitHub and collaboration (Lessons 15–16)
83. What is a remote? What is `origin`?
84. `git push` vs `git pull` vs `git clone`.
85. `git fetch` vs `git pull`.
86. Why didn't we tick "Add a README" when creating the GitHub repository?
87. What is a branch and why do teams use branches?
88. Fast-forward merge vs merge commit.
89. What is a merge conflict, and what do `<<<<<<<`, `=======` and `>>>>>>>` mean?
90. What is a pull request? Name four things a team can do on a PR page.
91. What should a good PR description contain?
92. Collaborators vs forks.
93. What is branch protection?
94. What sections should a good README have?

## Section H — Docker (Lessons 17–19)
95. What problem does Docker solve?
96. Virtual machine vs container (three differences).
97. Image vs container.
98. What is Docker Hub? What is a tag?
99. What do these flags mean: `-d`, `-it`, `--rm`, `-p 8080:80`, `-e KEY=value`, `--name`, `-v`?
100. Why is port mapping needed?
101. `docker ps` vs `docker ps -a`.
102. What does `docker exec` do?
103. What is a Dockerfile? Explain `FROM`, `WORKDIR`, `COPY`, `RUN`, `EXPOSE`, `CMD`.
104. `RUN` vs `CMD`.
105. Why copy `requirements.txt` and install packages **before** copying the code?
106. What is `.dockerignore` for? Name three things in it.
107. Why does uvicorn need `--host 0.0.0.0` inside a container?
108. How can one image run with different settings?
109. What happens to a container's data when you remove it? How do you keep it?
110. What is Docker Compose and why use it?
111. In Compose, why does the API connect to `db:5432` and not `localhost:5432`?
112. What do `depends_on` with `condition: service_healthy` and `healthcheck` do?
113. `docker compose down` vs `docker compose down -v`.
114. Why do you need `--build` after changing your code?
