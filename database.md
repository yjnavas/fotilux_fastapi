Table user {Table user {
  id integer (PK)
  name varchar
  mail varchar
  password varchar
  created_at timestamp
}

Table post {
  id integer (PK)
  title varchar
  body text [note: 'Content of the post']
  user_id integer
  status varchar
  created_at timestamp
}

Table media {  // Nueva tabla para gestionar imágenes
  id integer (PK)
  url string       // URL de la imagen
  created_at timestamp
  entity_type varchar  // 'user' o 'post'
  entity_id integer    // ID de la entidad correspondiente
}

Table comment {
  id integer (PK)
  content varchar
  created_at timestamp
  post_id integer
  user_id integer
}

Table like {
  id integer (PK)
  post_id integer
  user_id integer
}

Table favorites {
  id integer (PK)
  post_id integer
  user_id integer
}

Table follow {
  following_user_id integer
  followed_user_id integer
  created_at timestamp 
}

Ref: post.user_id > user.id
Ref: user.id > follow.following_user_id
Ref: user.id > follow.followed_user_id
Ref: user.id > comment.user_id
Ref: post.id > comment.post_id
Ref: post.id > like.post_id
Ref: user.id > like.user_id
Ref: user.id > favorites.user_id
Ref: post.id > favorites.post_id

// Nuevas relaciones para la tabla media
Ref: user.id > media.entity_id [condition: "entity_type = 'user'"]  // Usuario a media
Ref: post.id > media.entity_id [condition: "entity_type = 'post'"] // Post a media