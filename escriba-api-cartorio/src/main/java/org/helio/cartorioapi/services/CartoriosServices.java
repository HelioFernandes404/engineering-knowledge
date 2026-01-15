package org.helio.cartorioapi.services;

import org.helio.cartorioapi.dto.AtribuicaosDTO;
import org.helio.cartorioapi.dto.CartoriosDTO;
import org.helio.cartorioapi.dto.CartoriosMinDTO;
import org.helio.cartorioapi.dto.SituacaosDTO;
import org.helio.cartorioapi.entidades.Atribuicaos;
import org.helio.cartorioapi.entidades.Cartorios;
import org.helio.cartorioapi.entidades.Situacaos;
import org.helio.cartorioapi.repositorios.AtribuicaoRepository;
import org.helio.cartorioapi.repositorios.CartoriosRepository;
import org.helio.cartorioapi.repositorios.SituacaoRepository;
import org.helio.cartorioapi.services.exceptions.DatabaseException;
import org.helio.cartorioapi.services.exceptions.ResourceNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.dao.EmptyResultDataAccessException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class CartoriosServices {

    @Autowired
    private CartoriosRepository cartoriosRepository;
    @Autowired
    private AtribuicaoRepository atribuicaoRepository;
    @Autowired
    private SituacaoRepository situacaoRepository;
    @Autowired
    private SituacaosServices situacaosServices;
    @Autowired
    private AtribuicaosServices atribuicaosServices;

    @Transactional(readOnly = true)
    public Page<CartoriosMinDTO> findAll(Pageable pageable) {
        Page<Cartorios> result = cartoriosRepository.findAllBy(pageable);
        return result.map(x -> new CartoriosMinDTO(x));
    }

    @Transactional(readOnly = true)
    public Cartorios findById(Integer id) {
        Cartorios entity = cartoriosRepository.findById(id).orElseThrow(
                () -> new ResourceNotFoundException("Recurso não encontrado"));
        return entity;
    }

    @Transactional
    public CartoriosDTO insert(CartoriosDTO dto) {
        Optional<Cartorios> existingByNome = cartoriosRepository.findByNome(dto.getNome());
        if (existingByNome.isPresent()) {
            throw new DatabaseException("Nome já informado no registro com código: " + existingByNome.get().getId());
        }
        Cartorios entity = new Cartorios();
        copyDtoToEntity(dto, entity);
        entity = cartoriosRepository.save(entity);
        return new CartoriosDTO(entity);
    }


    @Transactional
    public CartoriosDTO update(Integer id, CartoriosDTO dto) {
        Optional<Cartorios> existing = cartoriosRepository.findById(id);
        if (!existing.isPresent()) {
            throw new DatabaseException("Registro com ID " + id + " não encontrado");
        }
        Cartorios entity = existing.get();
        if (!entity.getNome().equals(dto.getNome())) {
            Optional<Cartorios> duplicate = cartoriosRepository.findByNome(dto.getNome());
            if (duplicate.isPresent()) {
                throw new DatabaseException("Nome já informado no registro com código " + duplicate.get().getId());
            }
        }


        // Atualizando Cartorio
        entity.setId(dto.getId());
        entity.setNome(dto.getNome());
        entity.setObservacao(dto.getObservacao());


        // Atualizando a situação
        SituacaosDTO situacaosDTO = dto.getSituacao();
        Optional<Situacaos> situacaoOptional = situacaoRepository.findById(situacaosDTO.getId());
        Situacaos situacao;
        if (!situacaoOptional.isPresent()) {
            // Se a situação com o ID especificado não for encontrada, cria uma nova situação
            situacao = new Situacaos();
            situacao.setId(situacaosDTO.getId());
            situacao.setNome(situacaosDTO.getNome());
            // Aqui você pode definir outros campos da situação conforme necessário
            situacao = situacaoRepository.save(situacao);
        } else {
            // Se a situação for encontrada, atualiza o nome
            situacao = situacaoOptional.get();
            situacao.setNome(situacaosDTO.getNome());
            situacao = situacaoRepository.save(situacao);
        }
        entity.setSituacao(situacao);

        // Atualizando as atribuições
        List<Atribuicaos> atribuicaosList = new ArrayList<>();
        for (AtribuicaosDTO atribuicaoDTO : dto.getAtribuicoes()) {
            Optional<Atribuicaos> atribuicaoOptional = atribuicaoRepository.findById(atribuicaoDTO.getId());
            if (!atribuicaoOptional.isPresent()) {
                throw new DatabaseException("Atribuição com ID " + atribuicaoDTO.getId() + " não encontrada");
            }
            Atribuicaos atribuicao = atribuicaoOptional.get();
            atribuicao.setId(atribuicaoDTO.getId());
            atribuicao.setNome(atribuicaoDTO.getNome());
            atribuicao = atribuicaoRepository.save(atribuicao);
            atribuicaosList.add(atribuicao);
        }
        entity.setAtribuicoes(atribuicaosList);

        entity = cartoriosRepository.save(entity);
        return new CartoriosDTO(entity);
    }

    @Transactional(propagation = Propagation.SUPPORTS)
    public void delete(Integer id) {
        try {
            cartoriosRepository.deleteById(id);
        } catch (EmptyResultDataAccessException e) {
            throw new ResourceNotFoundException("Recurso não encontrado");
        } catch (DataIntegrityViolationException e) {
            throw new DatabaseException("Registro utilizado em outro cadastro");
        }
    }


    private void copyDtoToEntity(CartoriosDTO dto, Cartorios entity) {
        entity.setId(dto.getId());
        entity.setNome(dto.getNome());
        entity.setObservacao(dto.getObservacao());


        if (dto.getSituacao() != null) {
            Situacaos entitySituacaos = situacaoRepository.getReferenceById(dto.getSituacao().getId());
            entity.setSituacao(entitySituacaos);
        } else {
            Situacaos defaultSituacao = new Situacaos("SIT_BLOQUEADO", "Bloqueado", null);
            entity.setSituacao(defaultSituacao);
        }

        if (dto.getAtribuicoes() != null) {
            List<Atribuicaos> list = new ArrayList<>();
            for (AtribuicaosDTO atribuicaoDTO : dto.getAtribuicoes()) {
                Atribuicaos atribuicao = atribuicaoRepository.getReferenceById(atribuicaoDTO.getId());

                list.add(atribuicao);
            }
            entity.setAtribuicoes(list);
        } else {
            //Atribuicaos defaultAtribuicaos = new Atribuicaos();
            //entity.setAtribuicoes();
            entity.setAtribuicoes(new ArrayList<>());
        }
    }



    private Atribuicaos convertAtribuicaosDTOToAtribuicaos(AtribuicaosDTO atribuicaosDTO) {
        if (atribuicaosDTO == null) {
            return null;
        }
        Atribuicaos atribuicao = new Atribuicaos();
        // Copie os campos do DTO para a entidade aqui
        // Exemplo: atribuicao.setId(atribuicaosDTO.getId());
        atribuicao.setId(atribuicaosDTO.getId());
        atribuicao.setNome(atribuicaosDTO.getNome());
        atribuicao.setSituacao(atribuicao.isSituacao());
        return atribuicao;
    }

}
